import threading 
import time

class SleepyWorker(threading.Thread):

    def __init__(self,seconds , **kwargs):
        self._seconds = seconds
        super(SleepyWorker, self).__init__(**kwargs)
        self.start()

    def sleep_a_little(self):
        time.sleep(self._seconds)

    def run(self):
        self.sleep_a_little()

