import random
import threading
import time

class EventDriven:
    def __init__(self):
        self.data = 0
        self.thread = threading.Thread(target=self.daemon, daemon=True)

    def get_data(self):
        return self.data

    def start(self):
        if self.thread:
            self.thread.start()

    def stop(self):
        if self.thread:
            self.thread._stop()
    def getrandom(self):
        if

    def daemon(self):
        while True:
            try:
                self.data = random.random()
                # Push IDF data in daemon thread
                # self.dan.push(<idf_name:str>, <data:list>)
                time.sleep(10)
            except:
                pass