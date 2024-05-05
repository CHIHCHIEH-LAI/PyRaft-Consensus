from src.transaction import Transaction
from src.grpc_client import gRPCClient

class LogEntry:
    def __init__(self, leaderId: int, logTerm: int, logIndex: int, transaction: Transaction):
        self.leaderId = leaderId
        self.logTerm = logTerm
        self.logIndex = logIndex
        self.transaction = transaction

class LogManager:
    def __init__(self, nodeId: int, memberTable: dict, gRPC_client: gRPCClient):
        self.nodeId = nodeId
        self.memberTable = memberTable
        self.gRPC_client = gRPC_client
        self.entries: list[LogEntry] = []

    def get_last_index(self):
        if len(self.entries) == 0:
            return 0
        return self.entries[-1].logIndex
    
    def get_last_term(self):
        if len(self.entries) == 0:
            return 0
        return self.entries[-1].logTerm
    
    def is_more_up_to_date(self, lastLogIndex: int, lastLogTerm: int):
        if lastLogTerm > self.get_last_term():
            return True
        if lastLogTerm == self.get_last_term() and lastLogIndex >= self.get_last_index():
            return True
        return False
    
    async def add_transaction(self, term: int, transaction: dict):
        if term > self.get_last_term():
            logIndex = 0
        else:
            logIndex = self.get_last_index() + 1

        logEntry = LogEntry(
            leaderId=self.nodeId,
            logTerm=term,
            logIndex=logIndex,
            transaction=Transaction(**transaction)
        )
        
        self.append_log_entry(logEntry)

        await self.multicast_log_entry()
    
    def append_log_entry(self, logEntry: LogEntry):
        self.entries.append(logEntry)
        return True

    async def multicast_log_entry(self):
        entryRequest = {
            'leaderId': self.nodeId,
            'logTerm': self.get_last_term(),
            'logIndex': self.get_last_index(),
            'transaction': self.entries[-1].transaction.to_dict(),
            'prevLogTerm': self.entries[-2].logTerm if len(self.entries) > 1 else 0,
            'prevLogIndex': self.entries[-2].logIndex if len(self.entries) > 1 else 0,
        }
        for id, (host, port) in self.memberTable.items():
            if id != self.nodeId:
                await self.send_log_entry(host, port, entryRequest)
        return True

    async def send_log_entry(self, host: str, port: int, entryRequest: dict):
        success, missingLogTerm, missingLogIndex = await self.gRPC_client.make_append_entry_rpc(host, port, entryRequest)
        return success, missingLogTerm, missingLogIndex