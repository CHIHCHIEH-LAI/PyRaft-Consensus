from src.state_machine import StateMachine

class ElectionModule:
    def __init__(self, state_machine: StateMachine):
        self.state_machine = state_machine
        self.vote_count = 0
        self.voted_for = None

    def start_election(self):
        self.vote_count = 1
        self.voted_for = self.nodeId
        self.increment_current_term()
        self.transition_to_candidate()

    def on_vote_received(self):
        self.vote_count += 1
        if self.vote_count > self.node_count / 2:
            self.transition_to_leader()

    def get_vote_count(self):
        return self.vote_count
