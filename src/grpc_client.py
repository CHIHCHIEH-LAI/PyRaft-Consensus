import grpc
from src.proto import raft_pb2
from src.proto import raft_pb2_grpc
from src.raft_node import RaftNode

class gRPCClient:
    def __init__(self, raft_node: RaftNode):
        self.raft_node = raft_node

    def make_append_entry_rpc(self):
        pass

    def make_request_vote_rpc(self, url: str):
        with grpc.insecure_channel(url) as channel:
            stub = raft_pb2_grpc.RaftServiceStub(channel)
            response = stub.RequestVote(raft_pb2.VoteRequest())
            return response.voteGranted

    def make_add_transaction_rpc(self, url: str):
        pass