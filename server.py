import asyncio
from grpc import aio

from src.proto import raft_pb2_grpc
from src.channel.grpc_server import gRPCServer
from src.raft_node import RaftNode

async def serve(id: int,  memberTable: dict):
    raft_node = RaftNode(id, memberTable)

    host, port = memberTable[id]

    server = aio.server()
    raft_pb2_grpc.add_RaftServiceServicer_to_server(gRPCServer(), server)
    server.add_insecure_port(f'{host}:{port}')
    await server.start()

    await raft_node.run()
    await server.wait_for_termination()

if __name__ == '__main__':

    memberTable = {
        1: ('localhost', 50051),
        2: ('localhost', 50052),
        3: ('localhost', 50053),
        4: ('localhost', 50054),
        5: ('localhost', 50055)
    }

    servers = [
        serve(1, memberTable),
        serve(2, memberTable),
        serve(3, memberTable),
        serve(4, memberTable),
        serve(5, memberTable)
    ]

    asyncio.run(asyncio.gather(*servers))