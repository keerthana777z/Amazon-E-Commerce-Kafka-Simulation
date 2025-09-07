import streamlit as st
import pandas as pd
from pymongo import MongoClient
import requests

# --- Configuration ---
FLASK_API_URL = "http://127.0.0.1:5001"
client = MongoClient('mongodb://localhost:27017/')
db = client['ecommerce']
collection = db['orders']

# --- Page Setup ---
st.set_page_config(page_title="Admin Dashboard", layout="wide")
st.title("📦 Admin Order Management")

# --- Functions ---
def update_order_status(order_id, new_status):
    """Sends a request to the Flask API to update the order status."""
    try:
        response = requests.post(
            f"{FLASK_API_URL}/update-status",
            json={"order_id": order_id, "status": new_status}
        )
        if response.status_code == 200:
            st.success(f"Order {order_id} marked as {new_status}!")
        else:
            st.error("Failed to update status.")
    except requests.exceptions.ConnectionError:
        st.error("Connection Error: Is the Flask API running?")

# --- Display Orders ---
st.header("Current Orders")
orders_cursor = collection.find({}, {'_id': 0})
orders_list = list(orders_cursor)

if not orders_list:
    st.warning("No orders found.")
else:
    df = pd.DataFrame(orders_list)
    st.dataframe(df)

    st.header("Update Order Status")
    for order in orders_list:
        order_id = order['order_id']
        current_status = order['status']
        
        with st.expander(f"Order ID: {order_id} (Current Status: {current_status})"):
            st.write(order)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Mark as Packed", key=f"pack_{order_id}"):
                    update_order_status(order_id, "Packed")
            with col2:
                if st.button("Mark as Shipped", key=f"ship_{order_id}"):
                    update_order_status(order_id, "Shipped")
            with col3:
                if st.button("Mark as Delivered", key=f"deliver_{order_id}"):
                    update_order_status(order_id, "Delivered")
                    
if st.button("Refresh Orders"):
    st.rerun()