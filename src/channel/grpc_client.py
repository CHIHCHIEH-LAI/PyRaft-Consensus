import grpc
from src.channel.proto import raft_pb2, raft_pb2_grpc

class gRPCClient:

    async def make_append_entry_rpc(self, host: str, port: int, entryRequest: dict):
        url = self.construct_url(host, port)
        async with grpc.aio.insecure_channel(url) as channel:
            stub = raft_pb2_grpc.RaftServiceStub(channel)
            response = await stub.AppendEntry(raft_pb2.EntryRequest(**entryRequest))
            return response.success, response.missingLogTerm, response.missingLogIndex

    async def make_request_vote_rpc(self, host: str, port: int, voteRequest: dict):
        url = self.construct_url(host, port)
        async with grpc.aio.insecure_channel(url) as channel:
            stub = raft_pb2_grpc.RaftServiceStub(channel)
            response = await stub.RequestVote(raft_pb2.VoteRequest(**voteRequest))
            return response.voteGranted
        
    async def make_send_heartbeat_rpc(self, host: str, port: int, heartbeat: dict):
        url = self.construct_url(host, port)
        async with grpc.aio.insecure_channel(url) as channel:
            stub = raft_pb2_grpc.RaftServiceStub(channel)
            await stub.SendHeartbeat(raft_pb2.Heartbeat(**heartbeat))

    async def make_add_transaction_rpc(self, host: str, port: int, transaction: dict):
        url = self.construct_url(host, port)
        async with grpc.aio.insecure_channel(url) as channel:
            stub = raft_pb2_grpc.RaftServiceStub(channel)
            response = await stub.AddTransaction(raft_pb2.Transaction(transaction))
            return response.success
        
    def construct_url(self, host: str, port: int):
        return f'{host}:{port}'