from datetime import datetime
from random import randint

from src.grpc_client import gRPCClient

class HeartbeatManager:
    def __init__(self):
        self.heartbeatTimeout = randint(180, 240)
        self.lastHeartbeat = datetime.now()
        self.gRPC_client = gRPCClient()

    def has_timed_out(self):
        return (datetime.now() - self.lastHeartbeat).seconds > self.heartbeatTimeout
    
    def multicast_heartbeats(self, nodeId: int, heartbeat: dict):
        for id, (host, port) in self.memberTable.items():
            if id != nodeId:
                self.send_heartbeat(host, port, heartbeat)

    def send_heartbeat(self, host:str, port:int, heartbeat: dict):
        self.gRPC_client.make_send_heartbeat_rpc(host, port, heartbeat)
        self.lastHeartbeat = datetime.now()