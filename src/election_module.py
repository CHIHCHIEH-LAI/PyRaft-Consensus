from src.raft_node import RaftNode

class ElectionModule:
    def __init__(self, raft_node: RaftNode, memberTable: dict):
        self.log_manager = raft_node.log_manager
        self.gRPC_client = raft_node.gRPC_client
        self.state_machine = raft_node.state_machine
        self.memberTable = memberTable
        self.vote_count = 0
        self.leaderId = None

    async def run_election(self, nodeId: int, voteRequest: dict):
        self.vote_count = 1
        await self.multicast_vote_requests(nodeId, voteRequest)

    async def multicast_vote_requests(self, nodeId: int, voteRequest: dict):
        for id, (host, port) in self.memberTable.items():
            if id != nodeId:
                await self.send_vote_request(host, port, voteRequest)
                if self.has_won_election():
                    return True
        return False

    async def send_vote_request(self, host: str, port: int, voteRequest: dict):
        voteGranted = await self.gRPC_client.make_request_vote_rpc(host, port, voteRequest)
        if voteGranted:
            self.vote_count += 1

    def has_won_election(self):
        return self.vote_count > len(self.memberTable) // 2
    
    def respond_vote_request(self, term: int, lastLogIndex: int, lastLogTerm: int):
        if term > self.state_machine.get_current_term(): 
            if self.log_manager.is_more_up_to_date(lastLogIndex, lastLogTerm):
                self.state_machine.set_current_term(term)
                self.state_machine.to_follower()
                return True
        return False
    
    def update_leaderId(self, leaderId: int):
        self.leaderId = leaderId