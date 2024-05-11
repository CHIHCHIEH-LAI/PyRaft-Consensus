import asyncio
import logging

from src.raft_service import RaftService

# Configure the logging module
logging.basicConfig(level=logging.INFO)

async def start_service():
    memberTable = {
        1: ('localhost', 50051),
        2: ('localhost', 50052),
        3: ('localhost', 50053),
        4: ('localhost', 50054),
        5: ('localhost', 50055)
    }

    serves = []
    for id in range(1, 6):
        raft_service = RaftService(id, memberTable)
        serves.append(raft_service.serve())
    
    logging.info('Starting all servers')
    await asyncio.gather(*serves)
    logging.info('All servers terminated')

if __name__ == '__main__':

    asyncio.run(start_service())