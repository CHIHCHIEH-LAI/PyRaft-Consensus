import pytest
from unittest.mock import patch, AsyncMock
from src.channel.grpc_client import gRPCClient
from src.proto import raft_pb2, raft_pb2_grpc

@pytest.mark.asyncio
@patch('grpc.aio.insecure_channel')
@patch.object(raft_pb2_grpc, 'RaftServiceStub')
async def test_make_request_vote_rpc(mock_stub, mock_channel):
    # Create a gRPCClient
    client = gRPCClient()

    # Create an VoteRequest
    vote_request = {'term': 1, 'candidateId': 2, 'lastLogTerm': 3, 'lastLogIndex': 4}

    # Configure the mock stub to return a specific value when RequestVote is called
    mock_stub.return_value.RequestVote.return_value = raft_pb2.VoteResponse(voteGranted=True)

    # # Call make_request_vote_rpc
    response = await client.make_request_vote_rpc('localhost', 50051, vote_request)

    # # Assert that insecure_channel was called with the correct url
    # mock_channel.assert_called_once_with('localhost:50051')

    # Assert that RaftServiceStub was called with the correct channel
    # mock_stub.assert_called_once_with(mock_channel.return_value)

    # # Assert that RequestVote was called with the correct request
    # mock_stub.return_value.RequestVote.assert_called_once_with(raft_pb2.VoteRequest(**vote_request))

    # # Assert that the response is as expected
    # assert response.voteGranted == True