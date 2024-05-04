import asyncio
from grpc import aio

from src.proto import raft_pb2_grpc
from src.grpc_server import gRPCServer
from src.raft_node import RaftNode

async def serve(host, port):
    raft_node = RaftNode()
    await raft_node.start()

    server = aio.server()
    raft_pb2_grpc.add_RaftServiceServicer_to_server(gRPCServer(), server)
    server.add_insecure_port(f'{host}:{port}')
    await server.start()

    try:
        await raft_node.wait_for_termination()
        await server.wait_for_termination()
    except KeyboardInterrupt:
        await raft_node.stop()
        await server.stop(0)

if __name__ == '__main__':
    asyncio.run(serve(host='localhost', port=50051))