import streamlit as st
import pandas as pd
from datetime import datetime
import qrcode
from PIL import Image

# Streamlit app title
st.title("Casting and Transaction Management Application")

# Input fields
casting_number = st.text_input("Enter Casting Number", "")
scale_number = st.selectbox("Select Scale Number", options=["S1", "S2", "S3", "S4"])
bundle_size = st.number_input("Enter Bundle Size", min_value=1, step=1)

# Concatenate Casting Number and Scale Number to create a unique ID
if casting_number and scale_number:
    base_id = f"{casting_number}_{scale_number}"
    st.write(f"Generated ID: **{base_id}**")
else:
    st.warning("Please enter a valid Casting Number and Scale Number to generate an ID.")

# Placeholder for storing transaction data
if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame(columns=["Transaction ID", "Weight", "Date & Time", "Bundle Size"])

# Add Transaction
st.write("### Add Transaction")
weight = st.number_input("Enter Weight for Transaction", min_value=0.0, step=0.1)
if st.button("Add Transaction"):
    # Generate transaction ID
    transaction_count = len(st.session_state.transactions) + 1
    transaction_id = f"{base_id}_{str(transaction_count).zfill(3)}"

    # Capture current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Append the transaction to the DataFrame
    new_transaction = pd.DataFrame({
        "Transaction ID": [transaction_id],
        "Weight": [weight],
        "Date & Time": [current_datetime],
        "Bundle Size": [bundle_size]
    })
    st.session_state.transactions = pd.concat([st.session_state.transactions, new_transaction], ignore_index=True)

    st.success(f"Transaction {transaction_id} added successfully with weight {weight}.")

# Display Transactions
st.write("### Transaction Log")
st.dataframe(st.session_state.transactions)

# Generate QR Code for the latest transaction
if not st.session_state.transactions.empty:
    st.write("### Generate QR Code for Latest Transaction")

    # Get the latest transaction data
    latest_transaction = st.session_state.transactions.iloc[-1]

    # QR code data to include Transaction ID, Date & Time, and Bundle Size
    qr_data = (
        f"Transaction ID: {latest_transaction['Transaction ID']}\n"
        f"Date & Time: {latest_transaction['Date & Time']}\n"
        f"Bundle Size: {latest_transaction['Bundle Size']}"
    )

    # Generate QR code using QRCode object instead of make()
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_image = qr.make_image(fill="black", back_color="white").convert('RGB')

    # Display QR code and transaction information
    st.image(qr_image)
    st.write("**QR Code Information**")
    st.write(f"**Transaction ID:** {latest_transaction['Transaction ID']}")
    st.write(f"**Date & Time:** {latest_transaction['Date & Time']}")
    st.write(f"**Bundle Size:** {latest_transaction['Bundle Size']}")
