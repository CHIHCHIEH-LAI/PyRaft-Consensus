import grpc

from src.channel.proto import raft_pb2, raft_pb2_grpc
from src.raft_node import RaftNode
from src.consensus.log_manager import LogEntry
from src.schema.transaction import Transaction

class RaftService(raft_pb2_grpc.RaftServiceServicer):

    def __init__(self, raft_node: RaftNode):
        self.raft_node = raft_node

    async def AppendEntry(self, request, context):
        
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

    async def RequestVote(self, request, context):
        voteGranted = self.raft_node.respond_vote_request(
            term=request.term,
            lastLogIndex=request.lastLogIndex, 
            lastLogTerm=request.lastLogTerm
        )
        return raft_pb2.VoteResponse(voteGranted=voteGranted)
    
    async def SendHeartbeat(self, request, context):
        leaderId = request.leaderId
        term = request.term
        success = self.raft_node.respond_heartbeat(term, leaderId)
        return raft_pb2.HeartbeatResponse(success=success)

    async def AddTransaction(self, request, context):
        success = await self.raft_node.add_transaction()
        return raft_pb2.TransactionResponse(success=success)
    
class gRPCServer:
    def __init__(self, host: str, port: int, raft_node: RaftNode):
        self.raft_node = raft_node
        self.server = grpc.aio.server()
        raft_pb2_grpc.add_RaftServiceServicer_to_server(RaftService(raft_node), self.server)
        self.server.add_insecure_port(f'{host}:{port}')

    async def start(self):
        await self.server.start()
        await self.server.wait_for_termination()
