import time
import random

class StateMachine:
    def __init__(self):
        self.state = "follower"
        self.term = 0
        self.reset_heartbeat()

    def reset_heartbeat(self):
        self.last_heartbeat = time.time()
        self.heartbeat_timeout = random.uniform(10, 30)  # in seconds

    def respond_voteRequest(self, term):
        if term <= self.term:
            return False
        self.term = term
        return True
    
    def operate(self):
        if self.state == "follower":
            if self.should_become_candidate():
                self.become_candidate()
        elif self.state == "candidate":
            pass
        elif self.state == "leader":
            pass
    
    def should_become_candidate(self):
        return time.time() - self.last_heartbeat > self.heartbeat_timeout
    
    def become_candidate(self):
        self.state = "candidate"
        self.term += 1
        self.reset_heartbeat() 

    def add_logEntry(self):
        pass

    
    
