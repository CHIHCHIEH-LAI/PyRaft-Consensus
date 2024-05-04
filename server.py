from concurrent import futures
import grpc

from src.proto import raft_pb2
from src.proto import raft_pb2_grpc
from src.grpc_server import gRPCServer
from src.raft_node import RaftNode

def serve(host, port):
    raft_node = RaftNode()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    raft_pb2_grpc.add_InternalRaftServiceServicer_to_server(gRPCServer(raft_node), server)
    server.add_insecure_port(f'{host}:{port}')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve(host='localhost', port=50051)