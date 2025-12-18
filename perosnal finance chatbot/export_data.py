import pandas as pd
import sqlite3
from datetime import datetime
import os

DB_PATH = "expenses.db"   # MUST match main.py & charts.py


def _df_from_db():
    if not os.path.exists(DB_PATH):
        return pd.DataFrame()

    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(
            "SELECT id, amount, category, note, timestamp FROM expenses ORDER BY timestamp DESC",
            conn
        )
    except Exception as e:
        print("Export error:", e)
        df = pd.DataFrame()
    finally:
        conn.close()

    return df


def export_csv(path=None):
    df = _df_from_db()
    if df.empty:
        return "No data"

    if path is None:
        path = f"expenses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    df.to_csv(path, index=False)
    return path


def export_xlsx(path=None):
    df = _df_from_db()
    if df.empty:
        return "No data"

    if path is None:
        path = f"expenses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

    df.to_excel(path, index=False, engine="openpyxl")
    return path
