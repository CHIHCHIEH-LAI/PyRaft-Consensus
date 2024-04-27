from src.schema.transaction import Transaction

class LogEntry:
    def __init__(self, logTerm, logIndex, transaction: Transaction):
        self.logTerm = logTerm
        self.logIndex = logIndex
        self.transaction = transaction

class LogTable:
    def __init__(self):
        self.logs: []

    def add_log(self, logTerm, logIndex, transaction: Transaction): 
        self.logs.append(LogEntry(logTerm, logIndex, transaction))