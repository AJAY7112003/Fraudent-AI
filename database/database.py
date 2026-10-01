import sqlite3
from datetime import datetime

DB_PATH = "database/fraudnet.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # Account table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            account_id TEXT PRIMARY KEY,
            holder_name TEXT NOT NULL,
            mobile_number TEXT NOT NULL
        )
    """)

    # Transactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (

            transaction_id TEXT PRIMARY KEY,

            sender_id TEXT NOT NULL,
            receiver_id TEXT NOT NULL,

            amount REAL NOT NULL,
            transaction_type TEXT NOT NULL,

            device_id TEXT,

            latitude REAL,
            longitude REAL,
            location_accuracy REAL,
            location_name TEXT,

            timestamp TEXT NOT NULL,

            xgb_probability REAL,
            xgb_prediction INTEGER,

            anomaly_score REAL,
            anomaly_prediction INTEGER,

            risk_score REAL,
            risk_level TEXT,

            classification TEXT,

            status TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_account(account_id, holder_name, mobile_number):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO accounts
        (account_id, holder_name, mobile_number)
        VALUES (?, ?, ?)
    """, (
        account_id,
        holder_name,
        mobile_number
    ))

    conn.commit()
    conn.close()


def get_mobile_number(account_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT mobile_number
        FROM accounts
        WHERE account_id = ?
    """, (account_id,))

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return None


def save_transaction(data):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions (
            transaction_id,
            sender_id,
            receiver_id,
            amount,
            transaction_type,
            device_id,
            latitude,
            longitude,
            location_accuracy,
            location_name,
            timestamp,
            xgb_probability,
            xgb_prediction,
            anomaly_score,
            anomaly_prediction,
            risk_score,
            risk_level,
            classification,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["transaction_id"],
        data["sender_id"],
        data["receiver_id"],
        data["amount"],
        data["transaction_type"],
        data["device_id"],
        data["latitude"],
        data["longitude"],
        data["location_accuracy"],
        data["location_name"],
        data["timestamp"],
        data["xgb_probability"],
        data["xgb_prediction"],
        data["anomaly_score"],
        data["anomaly_prediction"],
        data["risk_score"],
        data["risk_level"],
        data["classification"],
        data["status"]
    ))

    conn.commit()
    conn.close()


def update_status(transaction_id, status):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE transactions
        SET status = ?
        WHERE transaction_id = ?
    """, (
        status,
        transaction_id
    ))

    conn.commit()
    conn.close()


def get_all_transactions():

    conn = get_connection()

    query = """
        SELECT *
        FROM transactions
        ORDER BY timestamp DESC
    """

    import pandas as pd

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df