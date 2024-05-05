import asyncio
from grpc import aio

from src.proto import raft_pb2_grpc
from src.grpc_server import gRPCServer
from src.raft_node import RaftNode

async def serve(host, port):
    raft_node = RaftNode()

    server = aio.server()
    raft_pb2_grpc.add_RaftServiceServicer_to_server(gRPCServer(), server)
    server.add_insecure_port(f'{host}:{port}')
    await server.start()

    await raft_node.run()
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve(host='localhost', port=50051))