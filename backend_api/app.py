from flask import Flask, request, jsonify
from kafka import KafkaProducer
from pymongo import MongoClient
import json
import time
import random
from flask_cors import CORS # Import CORS

app = Flask(__name__)
CORS(app) # ✅ Enable CORS for the entire app

# Kafka Producer Configuration
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# MongoDB Client Configuration
client = MongoClient('mongodb://localhost:27017/')
db = client['ecommerce']
orders_collection = db['orders']

@app.route('/place-order', methods=['POST'])
def place_order():
    """API endpoint for users to place an order."""
    order_details = request.get_json()
    order_id = int(time.time() * 1000) # Simple unique ID

    order_data = {
        "order_id": order_id,
        "user_id": order_details.get("user_id", f"USER_{random.randint(1, 100)}"),
        "items": order_details.get("items", []), 
        "amount": order_details.get("amount", 0),
        "image": order_details.get("image", "https://via.placeholder.com/150"), # <<< ADD THIS LINE
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

@app.route('/update-status', methods=['POST'])
def update_status():
    """API endpoint for admins to update an order's status."""
    update_details = request.get_json()
    order_id = update_details.get("order_id")
    new_status = update_details.get("status")

    status_update_data = {
        "order_id": order_id,
        "status": new_status,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S") # Consistent timestamp format
    }
    
    producer.send('order-status', status_update_data)
    producer.flush()
    print(f"✅ Status update for order {order_id} sent to Kafka.")

    return jsonify({"message": f"Status for order {order_id} updated to {new_status}"})

@app.route('/order-status/<int:order_id>', methods=['GET'])
def get_order_status(order_id):
    """API endpoint to fetch the current status and history of an order."""
    order = orders_collection.find_one({'order_id': order_id}, {'_id': 0})
    if order:
        return jsonify(order)
    else:
        return jsonify({"error": "Order not found"}), 404

# ✅ NEW ENDPOINT FOR THE REACT FRONTEND
@app.route('/orders', methods=['GET'])
def get_user_orders():
    """API endpoint to fetch all orders for a specific user."""
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    orders_cursor = orders_collection.find({'user_id': user_id}, {'_id': 0})
    orders = list(orders_cursor)

    return jsonify(orders)


if __name__ == '__main__':
    app.run(port=5001, debug=True) # Your API runs on port 5001