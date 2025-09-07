from kafka import KafkaConsumer
from pymongo import MongoClient
import json

consumer = KafkaConsumer(
    'order-status',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='status-update-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

client = MongoClient('mongodb://localhost:27017/')
db = client['ecommerce']
collection = db['orders']

print("⏳ Status Consumer: Listening for status updates...")
for message in consumer:
    update = message.value
    order_id = update['order_id']
    new_status = update['status']
    timestamp = update['timestamp']
    
    print(f"📩 Received status update for {order_id}: {new_status}")
    
    # ✅ Update the status and push the new event to the history array
    collection.update_one(
        {'order_id': order_id},
        {
            '$set': {'status': new_status},
            '$push': {'history': {"status": new_status, "timestamp": timestamp}}
        }
    )
    print("✅ Updated in MongoDB with history.")