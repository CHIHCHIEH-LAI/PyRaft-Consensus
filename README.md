# Distributed Stock Transaction Log with Raft Consensus (unfinished)
### Description
This project is a distributed system implementation for managing stock transactions using the Raft consensus algorithm. The Raft consensus algorithm is a protocol used for ensuring consistency across distributed systems. It allows a collection of machines to work as a coherent group that can survive the failures of some of its members.

The project is structured around several key classes:

`RaftNode`: Represents a node in the Raft consensus algorithm. Each node maintains a state machine, a log, and an election module. The state machine tracks the current state of the node (follower, candidate, or leader), the log stores the commands that the node has received, and the election module handles the election process.

`ElectionModule`: Handles the election process in the Raft consensus algorithm. It is responsible for starting elections, handling vote requests, and determining the outcome of elections.

`LogManager`: Manages the log of a Raft node. It is responsible for adding new entries to the log and replicating the log to other servers.

`gRPCServer`: Handles communication between nodes using gRPC. It is responsible for sending and receiving RPCs such as RequestVote and AppendEntries.

The project also includes a script for starting multiple servers concurrently using asyncio. Each server runs a Raft node and listens on a different port.

This implementation of Raft provides a foundation for building distributed systems that require strong consistency, such as distributed databases or distributed file systems. It can be extended with additional features such as log compaction, membership changes, and more.

Key Skills: asyncio, gRPC, Raft Consensus

### Improvement
- logic for dealing with missing log entry
- containerize raft nodes and deploy them by using K8s

### Command
- Generate Python gRPC Code: python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. raft.proto 

### Source
- raft: https://www.youtube.com/watch?v=IujMVjKvWP4
- asyncio: https://www.youtube.com/watch?v=K56nNuBEd0c, https://www.youtube.com/watch?v=brYsDi-JajI 
