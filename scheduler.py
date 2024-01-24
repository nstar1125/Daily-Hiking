import schedule
import time

from email_handler import make_email, send_email
from config import load_config

def event():
    subject, body, attach = make_email()
    send_email(subject, body, attach)

def initialize_scheduler(time):
    schedule.every().day.at(str(time)).do(event)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

def run_background():
    schedule_cfg = load_config("schedule")
    initialize_scheduler(schedule_cfg["time"])
    run_scheduler()

if __name__ == "__main__":
    run_background()