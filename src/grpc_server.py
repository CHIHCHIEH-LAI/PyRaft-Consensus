from src.proto import raft_pb2
from src.proto import raft_pb2_grpc
from src.raft_node import RaftNode
from src.log import LogEntry
from src.transaction import Transaction

class gRPCServer(raft_pb2_grpc.RaftServiceServicer):

    def __init__(self, raft_node: RaftNode):
        self.raft_node = raft_node

    def AppendEntry(self, request, context):
        
        transaction = Transaction(
            userId=request.transaction.userId,
            stockId=request.transaction.stockId,
            quantity=request.transaction.quantity,
            price=request.transaction.price,
            timestamp=request.transaction.timestamp,
            transactionType=request.transaction.transactionType
        )

        log_entry = LogEntry(
            leaderId=request.leaderId,
            logTerm=request.logTerm,
            logIndex=request.logIndex,
            transaction=transaction
        )

        success, missingLogTerm, missingLogIndex = self.raft_node.append_log_entry(log_entry)
        return raft_pb2.EntryResponse(success=success, missingLogTerm=missingLogTerm, missingLogIndex=missingLogIndex)

    def RequestVote(self, request, context):
        voteGranted = self.raft_node.respond_vote_request(
            term=request.term,
            lastLogIndex=request.lastLogIndex, 
            lastLogTerm=request.lastLogTerm
        )
        return raft_pb2.VoteReponse(voteGranted=voteGranted)
    
    def SendHeartbeat(self, request, context):
        leaderId = request.leaderId
        term = request.term
        success = self.raft_node.respond_heartbeat(leaderId, term)
        return raft_pb2.HeartbeatResponse(success=success)

    def AddTransaction(self, request, context):
        success = self.raft_node.add_transaction()
        return raft_pb2.TransactionResponse(success=success)