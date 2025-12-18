from plyer import notification
import schedule
import time
import threading

def _notify(title, message):
    try:
        notification.notify(title=title, message=message, timeout=6)
    except Exception as e:
        print("Notification failed:", e)

def schedule_daily_reminder(hour, minute, message):
    # schedule daily at hour:minute UTC
    job_time = f"{hour:02d}:{minute:02d}"
    schedule.every().day.at(job_time).do(_notify, title="Finance Reminder", message=message)

def start_scheduler_thread():
    def run_loop():
        while True:
            schedule.run_pending()
            time.sleep(1)
    t = threading.Thread(target=run_loop, daemon=True)
    t.start()
    return t
