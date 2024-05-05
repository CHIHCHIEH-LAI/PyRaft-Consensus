from src.transaction import Transaction
from collections import defaultdict

class LogEntry:
    def __init__(self, leaderId: int, logTerm: int, logIndex: int, transaction: Transaction):
        self.leaderId = leaderId
        self.logTerm = logTerm
        self.logIndex = logIndex
        self.transaction = transaction

class Log:
    def __init__(self):
        self.entries = defaultdict(list)
        self.lastTerm = 0

    def get_last_index(self):
        return self.entries[self.lastTerm][-1].logIndex
    
    def get_last_term(self):
        return self.lastTerm
    
    def append_entry(self, log_entry: LogEntry):
        pass