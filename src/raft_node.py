import time

from src.consensus.heartbeat_manager import HeartbeatManager
from src.consensus.log_manager import LogManager, LogEntry
from src.consensus.state_machine import StateMachine
from src.consensus.election_module import ElectionModule
from src.channel.grpc_client import gRPCClient
from src.channel.grpc_server import gRPCServer

class RaftNode:
    def __init__(self, nodeId: int, memberTable: dict):
        self.nodeId = nodeId
        self.memberTable = memberTable
        self.log_manager = LogManager()
        self.gRPC_client = gRPCClient()
        self.gRPC_server = self.setup_gRPC_server()
        self.state_machine = StateMachine()
        self.election_module = ElectionModule(self, memberTable)
        self.heartbeat_manager = HeartbeatManager(self.gRPC_client, memberTable)

    def setup_gRPC_server(self):
        host, port = self.memberTable[self.nodeId]
        return gRPCServer(host, port, self)

    async def run(self):
        await self.gRPC_server.start()
        time.sleep(2)
        await self.run_node()
            
    async def run_node(self):
        while not self.state_machine.is_stopped():
            if self.state_machine.is_leader():
                await self.multicast_heartbeats()
            elif self.state_machine.is_follower():
                await self.wait_for_heartbeat()
            elif self.state_machine.is_candidate():
                await self.run_election()
            else:
                raise Exception('Invalid state')

    def stop(self):
        self.state_machine.to_stopped()

    def wait_for_heartbeat(self):
        if self.heartbeat_manager.has_timed_out():
            self.state_machine.to_candidate()

    async def run_election(self):
        voteRequest = {
            'term': self.state_machine.get_current_term(),
            'candidateId': self.nodeId,
            'lastLogIndex': self.log_manager.get_last_index(),
            'lastLogTerm': self.log_manager.get_last_term()
        }
        success = await self.election_module.run_election(self.nodeId, voteRequest)
        if success:
            self.election_module.update_leaderId(self.nodeId)
            self.state_machine.to_leader()
        else:
            self.state_machine.to_follower()

    def respond_vote_request(self, term: int, lastLogIndex: int, lastLogTerm: int):
        return self.election_module.respond_vote_request(
            term=term,
            lastLogIndex=lastLogIndex, 
            lastLogTerm=lastLogTerm
        )

    async def multicast_heartbeats(self):
        heartbeat = {
            'leaderId': self.nodeId,
            'term': self.state_machine.get_current_term()
        }
        await self.heartbeat_manager.multicast_heartbeats(self.nodeId, heartbeat)

    def respond_heartbeat(self, term: int, leaderId: int):
        if term >= self.state_machine.get_current_term():
            self.state_machine.set_current_term(term)
            self.state_machine.to_follower()
            self.heartbeat_manager.update_heartbeat()
            self.election_module.update_leaderId(leaderId)
            return True
        return False
    
    async def add_transaction(self, transaction: dict):
        if self.nodeId != self.election_module.leaderId:
            host, port = self.memberTable[self.election_module.leaderId]
            response = await self.gRPC_client.make_add_transaction_rpc(host, port, transaction)
            return response
        else:
            response = await self.log_manager.add_transaction(self.state_machine.get_current_term(), transaction)
            return response
        
    def append_log_entry(self, log_entry: LogEntry):
        success = self.log_manager.append_log_entry(log_entry)
        return success, 0, 0