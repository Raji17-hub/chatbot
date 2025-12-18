import sqlite3
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from datetime import datetime

DB_NAME = "expenses.db"   # ensure this is the SAME DB used everywhere

# ------------------- Helper to get data from DB -------------------
def _get_data():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT category, amount FROM expenses")
    rows = cur.fetchall()
    conn.close()
    return rows

# ------------------- Pie Chart -------------------
def show_pie_chart():
    rows = _get_data()
    if not rows:
        print("No expense data found.")
        return

    data = {}
    for cat, amt in rows:
        data[cat] = data.get(cat, 0) + amt

    plt.figure(figsize=(6,6))
    plt.pie(data.values(), labels=data.keys(), autopct="%1.1f%%")
    plt.title("Expense Distribution")
    plt.tight_layout()
    plt.show()

def show_yearly_pie_chart():
    show_pie_chart()

# ------------------- Bar Chart -------------------
def show_bar_chart():
    rows = _get_data()
    if not rows:
        print("No expense data found.")
        return

    data = {}
    for cat, amt in rows:
        data[cat] = data.get(cat, 0) + amt

    plt.figure(figsize=(8,6))
    plt.bar(data.keys(), data.values())
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.title("Expenses by Category")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()

def show_yearly_bar_chart():
    show_bar_chart()

# ------------------- Line Trend Chart -------------------
def show_line_trend():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # IMPORTANT: use timestamp column
    cur.execute("SELECT timestamp, amount FROM expenses ORDER BY timestamp")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No data available for line chart.")
        return

    # Parse FULL timestamp
    dates = [datetime.strptime(r[0], "%Y-%m-%d %H:%M:%S") for r in rows]
    amounts = [r[1] for r in rows]

    plt.figure(figsize=(10,5))
    plt.plot(dates, amounts, marker='o')
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Expense Trend")
    plt.gcf().autofmt_xdate()
    plt.gca().xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
    plt.tight_layout()
    plt.show()

def show_income_trend():
    show_line_trend()
