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
            userId = request.userId,
            stockId = request.stockId,
            quantity = request.quantity,
            price = request.price,
            timestamp = request.timestamp,
            transaction_type = request.transactionType
        )

        log_entry = LogEntry(
            leaderId = request.leaderId,
            logTerm = request.logTerm,
            logIndex = request.logIndex,
            transaction = transaction
        )

        success, missingLogTerm, missingLogIndex = self.raft_node.append_log_entry(log_entry)
        return raft_pb2.EntryResponse(success=success, missingLogTerm=missingLogTerm, missingLogIndex=missingLogIndex)

    def RequestVote(self, request, context):
        voteGranted = self.raft_node.respond_vote_request(request.term)
        return raft_pb2.VoteReponse(term=request.term, voteGranted=voteGranted)

    def AddTransaction(self, request, context):
        success = self.raft_node.add_transaction()
        return raft_pb2.TransactionResponse(success=success)