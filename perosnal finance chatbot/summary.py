from database import fetch_all, category_totals
from datetime import datetime, timedelta

def generate_summary():
    rows = fetch_all()
    if not rows:
        return "No expenses recorded."

    total = sum(r[1] for r in rows)
    last_7 = (datetime.utcnow() - timedelta(days=7)).isoformat()
    recent = [r for r in rows if r[4] >= last_7]
    recent_total = sum(r[1] for r in recent)
    cats = category_totals()
    top_cat = max(cats, key=lambda x: x[1]) if cats else ("-", 0)

    text = [
        f"Total saved in DB: ₹{total:.2f}",
        f"Last 7 days total: ₹{recent_total:.2f}",
        f"Top category: {top_cat[0]} (₹{top_cat[1]:.2f})",
        f"Entries stored: {len(rows)}"
    ]
    return "\n".join(text)
