import grpc
from src.channel.proto import raft_pb2, raft_pb2_grpc

def main():
    memberTable = {
        1: ('localhost', 50051),
        2: ('localhost', 50052),
        3: ('localhost', 50053),
        4: ('localhost', 50054),
        5: ('localhost', 50055)
    }

    id = 1
    host, port = memberTable[id]
    url = f'{host}:{port}'

    t = {
        'userId': 'client'+str(id),
        'stockId': 'AAPL',
        'quantity': 100,
        'price': 100.0,
        'timestamp': 1234567890,
        'transactionType': 0
    }

    with grpc.insecure_channel(url) as channel:
        stub = raft_pb2_grpc.RaftServiceStub(channel)
        response = stub.AddTransaction(raft_pb2.Transaction(**t))
        print(id, response.success)


if __name__ == '__main__':

    main()