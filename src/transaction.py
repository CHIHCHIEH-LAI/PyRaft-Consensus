import datetime
from enum import Enum

class TransactionType(Enum):
    BUY = 0
    SELL = 1

class Transaction:
    def __init__(self, userId: str, stockId: str, quantity: int, price: float, timestamp: datetime.datetime, transaction_type: TransactionType):
        self.userId = userId
        self.stockId = stockId
        self.quantity = quantity
        self.price = price
        self.timestamp = timestamp
        self.transaction_type = transaction_type