from datetime import datetime
from random import randint

from src.channel.grpc_client import gRPCClient

class HeartbeatManager:
    def __init__(self, gRPC_client: gRPCClient, memberTable: dict):
        self.heartbeatTimeout = randint(1, 10)
        self.lastHeartbeat = datetime.now()
        self.gRPC_client = gRPC_client
        self.memberTable = memberTable

    def has_timed_out(self):
        return (datetime.now() - self.lastHeartbeat).seconds > self.heartbeatTimeout
    
    async def multicast_heartbeats(self, nodeId: int, heartbeat: dict):
        for id, (host, port) in self.memberTable.items():
            if id != nodeId:
                await self.send_heartbeat(host, port, heartbeat)

    async def send_heartbeat(self, host:str, port:int, heartbeat: dict):
        await self.gRPC_client.make_send_heartbeat_rpc(host, port, heartbeat)
        self.update_heartbeat()

    def update_heartbeat(self):
        self.lastHeartbeat = datetime.now()