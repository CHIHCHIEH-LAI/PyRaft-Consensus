from src.log import Log, LogEntry
from src.state_machine import StateMachine
from src.election_module import ElectionModule

class RaftNode:
    def __init__(self, nodeId: int):
        self.nodeId = nodeId
        self.log = Log()
        self.state_machine = StateMachine()
        self.election_module = ElectionModule(self.state_machine)

    def start(self):
        pass

    def stop(self):
        pass

    def wait_for_termination(self):
        pass

    def append_log_entry(self, log_entry: LogEntry):
        self.log.append_entry(log_entry)
    
    def vote_for_candidate(self, candidate_id):
        self.election_module.vote_for_candidate(candidate_id)