import grpc
from src.proto import raft_pb2
from src.proto import raft_pb2_grpc

class gRPCClient:

    def make_append_entry_rpc(self, host: str, port: int):
        url = self.construct_url(host, port)
        

    async def make_request_vote_rpc(self, host: str, port: int, voteRequest: dict):
        url = self.construct_url(host, port)
        with grpc.insecure_channel(url) as channel:
            stub = raft_pb2_grpc.RaftServiceStub(channel)
            response = await stub.RequestVote(raft_pb2.VoteRequest(**voteRequest))
            return response.voteGranted
        
    async def make_send_heartbeat_rpc(self, host: str, port: int, heartbeat: dict):
        url = self.construct_url(host, port)
        with grpc.insecure_channel(url) as channel:
            stub = raft_pb2_grpc.RaftServiceStub(channel)
            await stub.SendHeartbeat(raft_pb2.Heartbeat(**heartbeat))

    def make_add_transaction_rpc(self, host: str, port: int, transaction: dict):
        url = self.construct_url(host, port)
        
    def construct_url(self, host: str, port: int):
        return f'{host}:{port}'