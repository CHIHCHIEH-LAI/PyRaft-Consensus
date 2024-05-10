from enum import Enum

class StateType(Enum):
    FOLLOWER = 1
    CANDIDATE = 2
    LEADER = 3
    STOPPED = 4

class StateMachine:
    def __init__(self):
        self.state = StateType.FOLLOWER
        self.currentTerm = 0

    def is_stopped(self):
        return self.state == StateType.STOPPED
    
    def is_leader(self):
        return self.state == StateType.LEADER

    def is_follower(self):
        return self.state == StateType.FOLLOWER
    
    def is_candidate(self):
        return self.state == StateType.CANDIDATE
    
    def to_stopped(self):
        self.state = StateType.STOPPED

    def to_leader(self):
        self.state = StateType.LEADER

    def to_follower(self):
        self.state = StateType.FOLLOWER

    def to_candidate(self):
        self.state = StateType.CANDIDATE
        self.set_current_term(self.get_current_term() + 1)

    def get_current_term(self):
        return self.currentTerm
    
    def set_current_term(self, term: int):
        self.currentTerm = term