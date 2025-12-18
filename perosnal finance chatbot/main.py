import tkinter as tk
from tkinter import ttk, scrolledtext, simpledialog, messagebox
from nlp_model import process_query
from reminders import schedule_daily_reminder, start_scheduler_thread
from export_data import export_csv, export_xlsx
import charts
import csv
from datetime import datetime
import os
from database import insert_expense, fetch_last, delete_by_id

# ------------------- CSV Import Function -------------------
CSV_FILE = "finance_data.csv"

def import_csv(file_path=CSV_FILE):
    if not os.path.exists(file_path):
        append_chat("Bot", "CSV file not found!")
        return

    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        count = 0
        for row in reader:
            row_type = row["Type"]         # Expense or Income
            category = row["Component"]
            value_str = row["Value"].replace("₹", "").replace(",", "").strip()
            try:
                amount = float(value_str)
            except:
                continue  # skip invalid numbers

            # Convert Date like "Jan-24" to timestamp
            month_str, year_suffix = row["Date"].split("-")
            month_num = datetime.strptime(month_str, "%b").month
            year = 2000 + int(year_suffix)
            timestamp = datetime(year, month_num, 1, 0, 0, 0).strftime("%Y-%m-%d %H:%M:%S")

            note = row_type
            insert_expense(amount, category, note)
            count += 1

    append_chat("Bot", f"✅ CSV imported successfully! {count} rows added.")

# ------------------- Start reminders scheduler -------------------
start_scheduler_thread()

# ------------------- Colors & Root -------------------
BG = "#0f1724"
CARD = "#0b1a2b"
ACCENT = "#1e90ff"
TEXT = "#e6eef6"

root = tk.Tk()
root.title("Personal Finance Manager Chatbot")
root.geometry("820x720")
root.configure(bg=BG)

style = ttk.Style()
style.theme_use('clam')
style.configure("TFrame", background=BG)
style.configure("TButton", background=ACCENT, foreground=TEXT, padding=6)
style.configure("TLabel", background=BG, foreground=TEXT)
style.configure("TEntry", fieldbackground=CARD, background=CARD, foreground=TEXT)
style.map("TButton", background=[('active', '#4aa3ff')])

# ------------------- Layout Frames -------------------
left = ttk.Frame(root, width=520, height=700)
left.pack(side=tk.LEFT, fill=tk.BOTH, padx=12, pady=12)
right = ttk.Frame(root, width=280, height=700)
right.pack(side=tk.RIGHT, fill=tk.Y, padx=12, pady=12)

# ------------------- Chat Area -------------------
chat_area = scrolledtext.ScrolledText(left, wrap=tk.WORD, width=60, height=28, bg=CARD, fg=TEXT, insertbackground=TEXT)
chat_area.pack(padx=8, pady=8)
chat_area.config(state=tk.DISABLED)
chat_area.tag_config("user", foreground="#00ff00")
chat_area.tag_config("bot", foreground=ACCENT)

def append_chat(who, text):
    chat_area.config(state=tk.NORMAL)
    tag = "user" if who == "You" else "bot"
    chat_area.insert(tk.END, f"{who}: {text}\n\n", tag)
    chat_area.see(tk.END)
    chat_area.config(state=tk.DISABLED)

# ------------------- Input Frame -------------------
input_frame = ttk.Frame(left)
input_frame.pack(padx=8, pady=(0,10), fill=tk.X)
input_box = ttk.Entry(input_frame)
input_box.pack(side=tk.LEFT, fill=tk.X, expand=True)
send_btn = ttk.Button(input_frame, text="Send")
send_btn.pack(side=tk.LEFT, padx=6)

def send_message():
    user_msg = input_box.get().strip()
    if not user_msg:
        return
    append_chat("You", user_msg)
    input_box.delete(0, tk.END)
    response = process_query(user_msg)
    append_chat("Bot", response)

send_btn.config(command=send_message)
input_box.bind("<Return>", lambda event: send_message())

# ------------------- Quick Action Buttons -------------------
ttk.Label(right, text="Quick Actions").pack(pady=(6,12))

def delete_last_expense():
    last = fetch_last(1)
    if last:
        delete_by_id(last[0][0])
        append_chat("Bot", "Last expense deleted successfully!")
    else:
        append_chat("Bot", "No expenses to delete.")

btns = [
    ("Show Expenses", lambda: append_chat("Bot", process_query("show expenses"))),
    ("Pie Chart", charts.show_pie_chart),
    ("Bar Chart", charts.show_bar_chart),
    ("Trend Chart", charts.show_line_trend),
    ("Summary", lambda: append_chat("Bot", process_query("summary"))),
    ("Delete Last", delete_last_expense),
    ("Export CSV", lambda: append_chat("Bot", f"CSV -> {export_csv()}")),
    ("Export Excel", lambda: append_chat("Bot", f"Excel -> {export_xlsx()}")),
    ("Import CSV", lambda: import_csv()),
]

for t, cmd in btns:
    ttk.Button(right, text=t, command=cmd).pack(fill=tk.X, padx=8, pady=6)

# ------------------- Reminders -------------------
def add_daily_reminder():
    hour = simpledialog.askinteger("Hour (0-23)", "Hour (UTC):", minvalue=0, maxvalue=23)
    if hour is None: return
    minute = simpledialog.askinteger("Minute (0-59)", "Minute:", minvalue=0, maxvalue=59)
    if minute is None: return
    msg = simpledialog.askstring("Reminder message", "Message to show:")
    if not msg: msg = "Time to review your finances!"
    schedule_daily_reminder(hour, minute, msg)
    messagebox.showinfo("Reminder", f"Daily reminder set at {hour:02d}:{minute:02d} UTC")

ttk.Button(right, text="Add Daily Reminder", command=add_daily_reminder).pack(fill=tk.X, padx=8, pady=6)

# ------------------- Sample Commands -------------------
ttk.Label(right, text="Sample Commands", font=("Arial", 10, "bold")).pack(pady=(12,4))
samples = [
    "Add expense 300 for groceries",
    "Show expenses",
    "Show pie chart",
    "Export csv",
    "Summary",
    "Delete last"
]
for s in samples:
    ttk.Label(right, text=s).pack(anchor="w", padx=8)

# ------------------- Charts -------------------
ttk.Label(right, text="Charts", font=("Arial", 10, "bold")).pack(pady=(12,4))
chart_btns = [
    ("Yearly Bar Chart", charts.show_yearly_bar_chart),
    ("Yearly Pie Chart", charts.show_yearly_pie_chart),
    ("Income Trend Line Chart", charts.show_income_trend)
]
for t, cmd in chart_btns:
    ttk.Button(right, text=t, command=cmd).pack(fill=tk.X, padx=8, pady=6)

# ------------------- Run App -------------------
root.mainloop()

