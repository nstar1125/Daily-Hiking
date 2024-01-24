from threading import Thread
from scheduler import run_background
from client import run_client

if __name__ == "__main__":
    monitoring_thread = Thread(target=run_background)
    monitoring_thread.setDaemon(True)
    monitoring_thread.start()
    run_client()