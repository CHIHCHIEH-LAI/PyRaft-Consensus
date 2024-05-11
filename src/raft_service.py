import asyncio
from loguru import logger
import grpc

from src.raft_node import RaftNode
from src.channel.proto import raft_pb2_grpc
from src.channel.grpc_server import gRPCServer

class RaftService:
    def __init__(self, id: int, memberTable: dict):
        self.id = id
        logger.info(f'Starting server {id}')
        self.raft_node = RaftNode(id, memberTable)
        self.server = grpc.aio.server()

        raft_pb2_grpc.add_RaftServiceServicer_to_server(gRPCServer(self.raft_node), self.server)
        host, port = memberTable[id]
        self.server.add_insecure_port(f'{host}:{port}')

    async def serve(self):
        await self.server.start()
        logger.info(f'Server {self.id} started')
        await asyncio.sleep(5)
        await self.raft_node.run()
        logger.info(f'Raft node {self.id} running')
        await self.server.wait_for_termination()
        logger.info(f'Server {self.id} terminated')


