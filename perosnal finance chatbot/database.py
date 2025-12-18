import sqlite3
from datetime import datetime

# ✅ ONE DB FILE – DO NOT CHANGE THIS
DB_PATH = "expenses.db"

# ✅ SINGLE CONNECTION (persistent)
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cur = conn.cursor()

# ✅ Create table (SAFE – does NOT delete data)
cur.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    category TEXT,
    note TEXT,
    timestamp TEXT
)
""")
conn.commit()


# ➕ Add expense (PERMANENT SAVE)
def insert_expense(amount, category, note=""):
    cur.execute(
        """
        INSERT INTO expenses (amount, category, note, timestamp)
        VALUES (?, ?, ?, ?)
        """,
        (
            amount,
            category,
            note,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )
    conn.commit()


# 📄 Fetch all expenses (FOR UI TABLE)
def fetch_all():
    cur.execute(
        "SELECT id, amount, category, note, timestamp FROM expenses ORDER BY timestamp DESC"
    )
    return cur.fetchall()


# ⏳ Fetch last N expenses
def fetch_last(n):
    cur.execute(
        "SELECT id, amount, category, note, timestamp FROM expenses ORDER BY timestamp DESC LIMIT ?",
        (n,)
    )
    return cur.fetchall()


# 📅 Fetch expenses between two dates
def fetch_between(start_date, end_date):
    cur.execute(
        """
        SELECT id, amount, category, note, timestamp
        FROM expenses
        WHERE timestamp BETWEEN ? AND ?
        ORDER BY timestamp DESC
        """,
        (start_date, end_date)
    )
    return cur.fetchall()


# ❌ Delete expense by ID (PERMANENT DELETE)
def delete_by_id(expense_id):
    cur.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )
    conn.commit()


# ✏️ Update expense
def update_expense(expense_id, amount, category, note=""):
    cur.execute(
        """
        UPDATE expenses
        SET amount = ?, category = ?, note = ?
        WHERE id = ?
        """,
        (amount, category, note, expense_id)
    )
    conn.commit()


# 📊 Category totals (FOR CHARTS)
def category_totals():
    cur.execute(
        """
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
        """
    )
    return cur.fetchall()
