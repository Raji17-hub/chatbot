import csv
from datetime import datetime
from db import insert_expense  # Your database module

csv_file = "finance_data.csv"

with open(csv_file, newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        row_type = row["Type"]         # Expense or Income
        category = row["Component"]
        value_str = row["Value"].replace("₹", "").replace(",", "").strip()
        try:
            amount = float(value_str)
        except:
            continue  # skip invalid numbers

        # Convert Date like "Jan-24" to timestamp (day=1, time=00:00:00)
        month_str, year_suffix = row["Date"].split("-")
        month_num = datetime.strptime(month_str, "%b").month
        year = 2000 + int(year_suffix)
        timestamp = datetime(year, month_num, 1, 0, 0, 0).strftime("%Y-%m-%d %H:%M:%S")

        note = row_type  # store Expense/Income as note

        # Insert into DB with correct timestamp
        insert_expense(amount, category, note, timestamp)

print("✅ CSV imported into expenses.db successfully!")
