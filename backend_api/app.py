from flask import Flask, request, jsonify
from kafka import KafkaProducer
from pymongo import MongoClient
import json
import time
import random
from flask_cors import CORS
from flask_bcrypt import Bcrypt  # New import for password hashing
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager  # New imports for tokens

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)  # Initialize bcrypt

# --- JWT Configuration ---
# Change this "super-secret" key in a real project!
app.config["JWT_SECRET_KEY"] = "super-secret-key-for-my-amazon-clone"
jwt = JWTManager(app)

# --- Kafka Producer Configuration ---
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# --- MongoDB Client Configuration ---
client = MongoClient('mongodb://localhost:27017/')
db = client['ecommerce']
orders_collection = db['orders']
users_collection = db['users']  # New collection for users

# ==================================================
# === NEW AUTHENTICATION ENDPOINTS ===
# ==================================================

@app.route('/signup', methods=['POST'])
def signup():
    """API endpoint for new users to sign up."""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Check if user already exists
    existing_user = users_collection.find_one({'username': username})
    if existing_user:
        return jsonify({"error": "Username already taken"}), 400

    # Hash the password for security
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create new user document
    new_user = {
        "username": username,
        "password": hashed_password
    }
    users_collection.insert_one(new_user)

    return jsonify({"message": "User created successfully!"}), 201

@app.route('/login', methods=['POST'])
def login():
    """API endpoint for users to log in."""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Find the user in the database
    user = users_collection.find_one({'username': username})

    # Check if user exists and password is correct
    if user and bcrypt.check_password_hash(user['password'], password):
        # Create a JWT token for the user. We'll use their username as the "identity"
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    else:
        return jsonify({"error": "Invalid username or password"}), 401

# ==================================================
# === SECURED ORDER ENDPOINTS ===
# ==================================================

@app.route('/place-order', methods=['POST'])
@jwt_required()  # This route now requires a valid JWT
def place_order():
    """API endpoint for users to place an order."""
    
    # Get the user's identity from the JWT token
    current_user_username = get_jwt_identity()
    
    order_details = request.get_json()
    order_id = int(time.time() * 1000)

    order_data = {
        "order_id": order_id,
        "user_id": current_user_username,  # Use the username from the token
        "items": order_details.get("items", []),
        "amount": order_details.get("amount", 0),
        "image": order_details.get("image", "https://via.placeholder.com/150"),
        "status": "Placed",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "history": [
            {"status": "Placed", "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}
        ]
    }

    producer.send('orders', order_data)
    producer.flush()
    print(f"✅ Order {order_id} sent to Kafka.")
    
    return jsonify({"message": "Order placed successfully!", "order_id": order_id}), 201

@app.route('/orders', methods=['GET'])
@jwt_required()  # This route now requires a valid JWT
def get_user_orders():
    """API endpoint to fetch all orders for the logged-in user."""
    
    # Get the user's identity from the JWT token
    current_user_username = get_jwt_identity()

    orders_cursor = orders_collection.find({'user_id': current_user_username}, {'_id': 0})
    orders = list(orders_cursor)
    return jsonify(orders)

@app.route('/order-status/<int:order_id>', methods=['GET'])
@jwt_required()  # Secure this route as well
def get_order_status(order_id):
    """API endpoint to fetch the current status and history of an order."""
    current_user_username = get_jwt_identity()
    
    # Find the order and make sure it belongs to the logged-in user
    order = orders_collection.find_one(
        {'order_id': order_id, 'user_id': current_user_username}, 
        {'_id': 0}
    )
    
    if order:
        return jsonify(order)
    else:
        return jsonify({"error": "Order not found or you do not have permission"}), 404

# ==================================================
# === ADMIN ENDPOINT (Unchanged) ===
# ==================================================
@app.route('/update-status', methods=['POST'])
def update_status():
    """API endpoint for admins to update an order's status."""
    # This remains unsecured for simplicity, but in a real app, you'd add admin-level security
    update_details = request.get_json()
    order_id = update_details.get("order_id")
    new_status = update_details.get("status")

    status_update_data = {
        "order_id": order_id,
        "status": new_status,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    producer.send('order-status', status_update_data)
    producer.flush()
    print(f"✅ Status update for order {order_id} sent to Kafka.")

    return jsonify({"message": f"Status for order {order_id} updated to {new_status}"})

if __name__ == '__main__':
    app.run(port=5001, debug=True)