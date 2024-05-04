from typing import List
import datetime
from enum import Enum

class TransactionType(Enum):
    BUY = "buy"
    SELL = "sell"

class LogEntry:
    def __init__(self, user_id: str, stock_id: str, quantity: int, price: float, timestamp: datetime.datetime, transaction_type: TransactionType):
        self.user_id = user_id
        self.stock_id = stock_id
        self.quantity = quantity
        self.price = price
        self.timestamp = timestamp
        self.transaction_type = transaction_type

class Log:
    def __init__(self):
        self.entries: List[LogEntry] = []