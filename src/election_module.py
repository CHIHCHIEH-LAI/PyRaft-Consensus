from src.grpc_client import gRPCClient

class ElectionModule:
    def __init__(self, memberTable: dict):
        self.gRPC_client = gRPCClient()
        self.memberTable = memberTable
        self.vote_count = 0

    async def run_election(self, nodeId: int, voteRequest: dict):
        self.vote_count = 1
        await self.multicast_vote_requests(nodeId, voteRequest)

    async def multicast_vote_requests(self, nodeId: int, voteRequest: dict):
        for id, (host, port) in self.memberTable.items():
            if id != nodeId:
                await self.send_vote_request(host, port, voteRequest)
                if self.has_won_election():
                    return True

    async def send_vote_request(self, host: str, port: int, voteRequest: dict):
        voteGranted = await self.gRPC_client.make_request_vote_rpc(host, port, voteRequest)
        if voteGranted:
            self.vote_count += 1

    def has_won_election(self):
        return self.vote_count > len(self.memberTable) // 2