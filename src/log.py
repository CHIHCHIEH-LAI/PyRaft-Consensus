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
    
    def append_entry(self, log_entry: LogEntry):
        pass