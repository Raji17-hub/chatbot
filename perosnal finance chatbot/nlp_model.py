import sqlite3
from datetime import datetime
import re
import os
from database import insert_expense  # Your DB file

DB_FILE = "expenses.db"

def save_to_db(amount, category, tx_type):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    today = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute(
        "INSERT INTO expenses (amount, category, type, date) VALUES (?, ?, ?, ?)",
        (amount, category, tx_type, today)
    )
    conn.commit()
    conn.close()

def get_expenses():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, date, category, type, amount FROM expenses ORDER BY date DESC")
    rows = cur.fetchall()
    conn.close()
    result = ""
    for r in rows:
        result += f"{r[0]}: ₹{r[4]} | {r[2]} | {r[3]} | {r[1]}\n"
    return result if result else "No expenses yet."

def get_summary():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT type, SUM(amount) FROM expenses GROUP BY type")
    rows = cur.fetchall()
    conn.close()
    summary = ""
    for r in rows:
        summary += f"{r[0].capitalize()}: ₹{r[1]}\n"
    return summary if summary else "No data yet."

def delete_last():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id FROM expenses ORDER BY date DESC LIMIT 1")
    row = cur.fetchone()
    if row:
        cur.execute("DELETE FROM expenses WHERE id=?", (row[0],))
        conn.commit()
        conn.close()
        return f"Deleted last expense (id={row[0]})."
    else:
        conn.close()
        return "No expenses to delete."

def process_query(msg):
    msg = msg.lower()

    # Detect type explicitly
    if "income" in msg:
        tx_type = "income"
    elif "expense" in msg:
        tx_type = "expense"
    else:
        tx_type = None  # unknown type

    # Extract amount
    amounts = re.findall(r"\d+\.?\d*", msg)
    amount = float(amounts[0]) if amounts else None

    # Extract category
    if "for" in msg:
        category = msg.split("for")[-1].strip()
    else:
        category = "General"

    # Handle saving to DB
    if tx_type and amount:
        save_to_db(amount, category, tx_type)
        return f"Added {tx_type} ₹{amount} for {category}."
    elif not tx_type and amount:
        # if no type given, default to expense
        save_to_db(amount, category, "expense")
        return f"Added expense ₹{amount} for {category}."
    elif "show expenses" in msg:
        return get_expenses()
    elif "summary" in msg:
        return get_summary()
    elif "delete last" in msg:
        return delete_last()
    else:
        return ("I didn't understand. Examples:\n"
                "- Add expense 200 for food\n"
                "- Add income 5000 for salary\n"
                "- Show expenses\n"
                "- Summary\n"
                "- Delete last")
