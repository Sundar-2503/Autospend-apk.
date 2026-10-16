import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="Expense Tracker Dashboard", layout="wide")
st.title("📊 Automated SMS Expense Tracker Dashboard")

def load_data():
    conn = sqlite3.connect("expenses.db")
    df = pd.read_sql_query("SELECT * FROM expenses ORDER BY id DESC", conn)
    conn.close()
    return df

try:
    df = load_data()
    if not df.empty:
        col1, col2 = st.columns(2)
        col1.metric("Total Expenses Logged", f"₹ {df['amount'].sum():,.2f}")
        col2.metric("Total Transactions", len(df))
        
        st.subheader("Recent SMS Transactions")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No expenses logged yet. Scan your SMS from the Android app or send a test POST request!")
except Exception as e:
    st.warning("Database not initialized yet. Run `uvicorn backend_api:app --reload` first.")
