import asyncio

from src.raft_node import RaftNode

async def serve(id: int,  memberTable: dict):
    raft_node = RaftNode(id, memberTable)
    await raft_node.run()

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