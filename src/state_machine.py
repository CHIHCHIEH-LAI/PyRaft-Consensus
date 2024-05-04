from enum import Enum

class StateType(Enum):
    FOLLOWER = "follower"
    CANDIDATE = "candidate"
    LEADER = "leader"

class StateMachine:
    def __init__(self):
        self.state = StateType.FOLLOWER
        self.currentTerm = 0

    def transition_to_leader(self):
        self.state = StateType.LEADER

    def transition_to_follower(self):
        self.state = StateType.FOLLOWER

    def transition_to_candidate(self):
        self.state = StateType.CANDIDATE

    def get_state(self):
        return self.state

    def get_current_term(self):
        return self.currentTerm
    
    def increment_current_term(self):
        self.currentTerm += 1