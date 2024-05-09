import pytest
from unittest.mock import patch, AsyncMock
from src.grpc_client import gRPCClient
from src.proto import raft_pb2, raft_pb2_grpc

@patch('grpc.insecure_channel')
@patch.object(raft_pb2_grpc, 'RaftServiceStub')
def test_make_append_entry_rpc(mock_stub, mock_channel):
    # Create a gRPCClient
    client = gRPCClient()

    # Create an EntryRequest
    entry_request = {'leaderId': 1, 'logTerm': 2, 'logIndex': 3}

    # Configure the mock stub to return a specific value when AppendEntry is called
    mock_stub.return_value.AppendEntry.return_value = raft_pb2.AppendEntryResponse(success=True, missingLogTerm=0, missingLogIndex=0)

    # Call make_append_entry_rpc
    response = client.make_append_entry_rpc('localhost', 50051, entry_request)

    # Assert that insecure_channel was called with the correct url
    mock_channel.assert_called_once_with('localhost:50051')

    # Assert that RaftServiceStub was called with the correct channel
    mock_stub.assert_called_once_with(mock_channel.return_value)

    # Assert that AppendEntry was called with the correct request
    mock_stub.return_value.AppendEntry.assert_called_once_with(raft_pb2.EntryRequest(**entry_request))

    # Assert that the response is as expected
    assert response == (True, 0, 0)