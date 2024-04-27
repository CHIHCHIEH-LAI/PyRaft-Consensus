from src.server.log_schema.log_entry import LogEntry
from src.schema.transaction import Transaction

class LogTable:
    def __init__(self):
        self.logs: []

    def add_log(self, logTerm, logIndex, transaction: Transaction): 
        self.logs.append(LogEntry(logTerm, logIndex, transaction))