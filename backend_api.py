from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from datetime import datetime

app = FastAPI(title="Expense Tracker Backend")

def init_db():
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount REAL,
                    description TEXT,
                    timestamp TEXT
                )""")
    conn.commit()
    conn.close()

init_db()

class ExpenseItem(BaseModel):
    amount: float
    description: str

@app.post("/log-expense")
def log_expense(item: ExpenseItem):
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO expenses (amount, description, timestamp) VALUES (?, ?, ?)",
        (item.amount, item.description, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()
    return {"status": "success", "logged_amount": item.amount}

@app.get("/expenses")
def get_expenses():
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("SELECT id, amount, description, timestamp FROM expenses ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return [{"id": r[0], "amount": r[1], "description": r[2], "timestamp": r[3]} for r in rows]
