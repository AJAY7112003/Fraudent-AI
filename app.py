import streamlit as st

from database.database import create_tables

create_tables()

st.set_page_config(
    page_title="FraudNet AI",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ FraudNet AI")

st.write(
    "Intelligent Financial Fraud & Anomaly Detection System"
)

st.success(
    "Database initialized successfully."
)