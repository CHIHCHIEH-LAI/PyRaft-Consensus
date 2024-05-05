import datetime
from enum import Enum

class TransactionType(Enum):
    BUY = 0
    SELL = 1

class Transaction:
    def __init__(self, userId: str, stockId: str, quantity: int, price: float, timestamp: datetime.datetime, transactionType: TransactionType):
        self.userId = userId
        self.stockId = stockId
        self.quantity = quantity
        self.price = price
        self.timestamp = timestamp
        self.transactionType = transactionType

    def to_dict(self):
        return {
            'userId': self.userId,
            'stockId': self.stockId,
            'quantity': self.quantity,
            'price': self.price,
            'timestamp': self.timestamp,
            'transactionType': self.transactionType
        }