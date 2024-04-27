from concurrent import futures
import grpc
from src.channel import raft_pb2
from src.channel import raft_pb2_grpc

from src.server.raft_node import RaftNode

class InternalRaftService(raft_pb2_grpc.InternalRaftServiceServicer):

    def __init__(self, raft_node: RaftNode):
        self.raft_node = raft_node

    def RequestVote(self, request, context):
        voteGranted = self.raft_node.respondVoteRequest(request.term)
        return raft_pb2.VoteReponse(term=request.term, voteGranted=voteGranted)
    
    def AppendEntry(self, request, context):
        logTerm, logEntry, success = self.raft_node.add_logEntry(request)
        return raft_pb2.EntryResponse(logTerm=logTerm, logEntry=logEntry, success=success)
    
class ClientRaftService(raft_pb2_grpc.ClientRaftServiceServicer):

    def __init__(self, raft_node: RaftNode):
        self.raft_node = raft_node

    def AddTransaction(self, request, context):
        success = self.raft_node.add_Transaction(request)
        return raft_pb2.TransactionResponse(success=success)

def serve(host, port):
    raft_node = RaftNode()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    raft_pb2_grpc.add_InternalRaftServiceServicer_to_server(InternalRaftService(raft_node), server)
    raft_pb2_grpc.add_InternalRaftServiceServicer_to_server(ClientRaftService(raft_node), server)
    server.add_insecure_port(f'{host}:{port}')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve(host='localhost', port=50051)