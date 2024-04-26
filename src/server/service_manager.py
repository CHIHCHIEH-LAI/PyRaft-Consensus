import grpc
import threading

class ServerManager:
    def __init__(self, host, port, service):
        self.host = host
        self.port = port
        self.service = service  # The gRPC service implementation
        self.server = None

    def start(self):
        self.server = grpc.server(threading.ThreadPoolExecutor(max_workers=10))
        self.service.register(self.server)
        self.server.add_insecure_port(f'{self.host}:{self.port}')
        self.server.start()
        print(f'Server started on {self.host}:{self.port}')

    def stop(self):
        self.server.stop(0)
