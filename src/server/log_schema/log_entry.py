from src.schema.transaction import Transaction

class LogEntry:
    def __init__(self, logTerm, logIndex, transaction: Transaction):
        self.logTerm = logTerm
        self.logIndex = logIndex
        self.transaction = transaction

    