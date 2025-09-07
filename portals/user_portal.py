import streamlit as st
import requests
import random

# --- Configuration ---
FLASK_API_URL = "http://127.0.0.1:5001"

# --- Page Setup ---
st.set_page_config(page_title="Order Portal", layout="centered")
st.title("🛍️ Welcome to Our Store!")

# --- Place an Order Section ---
st.header("Place a New Order")
with st.form("order_form"):
    #user_id = st.text_input("Your User ID", value=f"USER_{random.randint(101, 200)}")
    user_id = st.text_input("Your User ID", value="USER_101")
    items = st.multiselect("Select Items", ["Laptop", "Mouse", "Keyboard", "Monitor"], default=["Laptop", "Mouse"])
    amount = st.number_input("Total Amount", min_value=100, max_value=100000, value=62000)
    
    submitted = st.form_submit_button("Place Order")
    if submitted:
        order_payload = {
            "user_id": user_id,
            "items": items,
            "amount": amount
        }
        try:
            response = requests.post(f"{FLASK_API_URL}/place-order", json=order_payload)
            if response.status_code == 201:
                order_id = response.json().get('order_id')
                st.success(f"Order placed successfully! Your Order ID is: **{order_id}**")
            else:
                st.error("Failed to place order.")
        except requests.exceptions.ConnectionError:
            st.error("Connection Error: Is the Flask API running?")

st.markdown("---")

# --- Track an Order Section ---
st.header("Track Your Order")
track_order_id = st.number_input("Enter your Order ID to track", format="%d", step=1)

if st.button("Track Order"):
    if track_order_id > 0:
        try:
            response = requests.get(f"{FLASK_API_URL}/order-status/{track_order_id}")
            if response.status_code == 200:
                status_data = response.json()
                st.success(f"Status for Order {track_order_id}: **{status_data['status']}**")
                st.json(status_data)
            else:
                st.error("Order not found.")
        except requests.exceptions.ConnectionError:
            st.error("Connection Error: Is the Flask API running?")
    else:
        st.warning("Please enter a valid Order ID.")