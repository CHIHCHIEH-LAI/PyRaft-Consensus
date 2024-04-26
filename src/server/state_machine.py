import time
import random

class StateMachine:
    def __init__(self):
        self.state = "follower"
        self.term = 0
        self.voted_for = None
        self.commit_index = 0
        self.last_applied = 0
        self.timeout_start = time.time()
        self.election_timeout = self.reset_election_timeout()

    def reset_election_timeout(self):
        return random.uniform(1.5, 3)  # Election timeout in seconds

    def update_state(self, new_state):
        self.state = new_state
        self.timeout_start = time.time()
        if new_state == "candidate":
            self.term += 1
            self.voted_for = None  # Candidate votes for itself in the actual election code

    def should_become_candidate(self):
        return time.time() - self.timeout_start > self.election_timeout
