import threading
import time

from src.server.state_machine import StateMachine

class RaftNode:
    def __init__(self):
        self.active = True
        self.thread = threading.Thread(target=self.run_task)
        self.thread.start()

    def run_task(self):
        while self.active:
            time.sleep(1)

    def stop(self):
        self.active = False
        self.thread.join()

    
