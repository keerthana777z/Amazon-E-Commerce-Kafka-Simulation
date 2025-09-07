# delete_all_orders.py

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# --- Configuration ---
MONGO_URI = 'mongodb://localhost:27017/'
DATABASE_NAME = 'ecommerce'
COLLECTION_NAME = 'orders'

def clear_all_orders():
    """Connects to MongoDB and deletes all documents in the orders collection."""
    try:
        # 1. Connect to the MongoDB client
        client = MongoClient(MONGO_URI)

        # 2. Select the database
        db = client[DATABASE_NAME]

        # 3. Select the collection
        collection = db[COLLECTION_NAME]

        print(f"Connecting to '{DATABASE_NAME}' database...")

        # 4. Delete all documents in the collection
        # The empty query {} matches all documents
        result = collection.delete_many({})

        # 5. Print the result
        print(f"✅ Success! Deleted {result.deleted_count} orders from the '{COLLECTION_NAME}' collection.")

    except ConnectionFailure as e:
        print(f"❌ Could not connect to MongoDB: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure the client connection is closed
        if 'client' in locals():
            client.close()

if __name__ == '__main__':
    # Add a confirmation step to prevent accidental deletion
    confirmation = input("⚠️ Are you sure you want to permanently delete all orders? (yes/no): ")
    if confirmation.lower() == 'yes':
        clear_all_orders()
    else:
        print("Operation cancelled.")