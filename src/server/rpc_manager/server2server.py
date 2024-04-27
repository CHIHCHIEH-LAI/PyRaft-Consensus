from src.channel import raft_pb2_grpc, raft_pb2

class RPCManager(raft_pb2_grpc.InternalRaftServiceServicer):
    def __init__(self, state_machine):
        self.state_machine = state_machine

    def register(self, server):
        raft_pb2_grpc.add_InternalRaftServiceServicer_to_server(self, server)

    def RequestVote(self, request, context):
        # Election voting logic here
        return raft_pb2.VoteResponse(term=self.state_machine.term, voteGranted=True)

    def AppendEntries(self, request, context):
        # Append entries logic here
        return raft_pb2.EntryResponse(term=self.state_machine.term, success=True)
