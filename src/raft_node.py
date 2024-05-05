from src.heartbeat_manager import HeartbeatManager
from src.log import Log, LogEntry
from src.state_machine import StateMachine
from src.election_module import ElectionModule

class RaftNode:
    def __init__(self, nodeId: int, memberTable: dict):
        self.nodeId = nodeId
        self.memberTable = memberTable
        self.log = Log()
        self.state_machine = StateMachine()
        self.election_module = ElectionModule(memberTable)
        self.heartbeat_manager = HeartbeatManager(memberTable)

    async def run(self):
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
            'lastLogIndex': self.log.get_last_index(),
            'lastLogTerm': self.log.get_last_term()
        }
        success = await self.election_module.run_election(self.nodeId, voteRequest)
        if success:
            self.state_machine.to_leader()
        else:
            self.state_machine.to_follower()        
    
    async def multicast_heartbeats(self):
        heartbeat = {
            
        }