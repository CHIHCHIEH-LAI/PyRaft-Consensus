import sys
import time

from src.server.state_machine import StateMachine
from src.server.rpc_manager import RPCManager
from src.server.server_manager import ServerManager

def main(host, port):
    state_machine = StateMachine()
    rpc_manager = RPCManager(state_machine)
    server_manager = ServerManager(host, port, rpc_manager)

    try:
        server_manager.start()
        while True:
            if state_machine.state == "follower" and state_machine.should_become_candidate():
                state_machine.update_state("candidate")
            time.sleep(0.1)
    except KeyboardInterrupt:
        server_manager.stop()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python raft_node.py host port")
        sys.exit(1)
    host = sys.argv[1]
    port = int(sys.argv[2])
    main(host, port)
