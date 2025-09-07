from kafka import KafkaConsumer
from pymongo import MongoClient
import json

consumer = KafkaConsumer(
    'orders',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='order-processing-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

client = MongoClient('mongodb://localhost:27017/')
db = client['ecommerce']
collection = db['orders']

print("⏳ Order Consumer: Listening for new orders...")
for message in consumer:
    order = message.value
    print(f"📩 Received new order: {order['order_id']}")
    collection.insert_one(order)
    print("✅ Stored in MongoDB.")
    