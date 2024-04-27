class Transaction:
    def __init__(self, userId, stockId, quantity, price, timestamp, transactionType):
        self.userId = userId
        self.stockId = stockId
        self.quantity = quantity
        self.price = price
        self.timestamp = timestamp
        self.transactionType = transactionType