import threading
import time
import grpc

from src.channel import raft_pb2
from src.channel import raft_pb2_grpc

from src.server.state_machine import StateMachine
from src.schema.transaction import Transaction
from src.server.log_table import LogTable

class RaftNode:
    def __init__(self, nodeId, serverList):
        self.active = True
        self.thread = threading.Thread(target=self.run_task)
        self.thread.start()
        self.nodeId = nodeId
        self.serverList = serverList
        self.state_machine = StateMachine()
        self.logTable = LogTable()

    def run_task(self):
        while self.active:
            self.operate()
            time.sleep(1)

    def stop(self):
        self.active = False
        self.thread.join()

    def operate(self):
        if self.state_machine.state == "follower":
            if self.state_machine.should_become_candidate():
                self.state_machine.become_candidate()
                if self.send_voteRequest():
                    self.state_machine.state = "leader"
                else:
                    self.state_machine.state = "follower"
            
    def send_voteRequest(self):
        numAgree = 0
        for server in self.serverList:
            with grpc.insecure_channel(server) as channel:
                stub = raft_pb2_grpc.InternalRaftServiceStub(channel)
                response = stub.RequestVote(raft_pb2.VoteRequest(
                    term=self.term, candidateId=1, lastLogIndex=0, lastLogTerm=0))
                if response.term == self.state_machine.term and response.voteGranted: numAgree += 1
        return numAgree > len(self.serverList) // 2
       
    def respond_voteRequest(self, request) -> bool:
        return self.state_machine.respond_voteRequest(request.term)
    
    def respond_entryRequest(self, request) -> tuple:
        leader_id = request.leaderId
        log_term = request.logTerm
        log_index = request.logIndex
        transaction = request.transaction
        prev_log_term = request.prevLogTerm
        prev_log_index = request.prevLogIndex

        user_id = transaction.userId
        stock_id = transaction.stockId
        quantity = transaction.quantity
        price = transaction.price
        timestamp = transaction.timestamp
        transaction_type = transaction.transactionType

        tran = Transaction(user_id, stock_id, quantity, price, timestamp, transaction_type)
        self.logTable.add_log(log_term, log_index, tran)
        


    def add_logEntry(self, request) -> tuple:
        pass

    # voteGranted = respondVoteRequest(request.term)
    # logTerm, logEntry, success = add_logEntry(request)
    # success = self.raft_node.add_Transaction(request)

    
