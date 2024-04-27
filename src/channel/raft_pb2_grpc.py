# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import raft_pb2 as raft__pb2


class ClientRaftServiceStub(object):
    """Service for client operations
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.AddEntry = channel.unary_unary(
                '/raft.ClientRaftService/AddEntry',
                request_serializer=raft__pb2.Transaction.SerializeToString,
                response_deserializer=raft__pb2.EntryResponse.FromString,
                )


class ClientRaftServiceServicer(object):
    """Service for client operations
    """

    def AddEntry(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ClientRaftServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'AddEntry': grpc.unary_unary_rpc_method_handler(
                    servicer.AddEntry,
                    request_deserializer=raft__pb2.Transaction.FromString,
                    response_serializer=raft__pb2.EntryResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'raft.ClientRaftService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ClientRaftService(object):
    """Service for client operations
    """

    @staticmethod
    def AddEntry(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/raft.ClientRaftService/AddEntry',
            raft__pb2.Transaction.SerializeToString,
            raft__pb2.EntryResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class InternalRaftServiceStub(object):
    """Service for Raft internal operations
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.AppendEntries = channel.unary_unary(
                '/raft.InternalRaftService/AppendEntries',
                request_serializer=raft__pb2.EntryRequest.SerializeToString,
                response_deserializer=raft__pb2.EntryResponse.FromString,
                )
        self.RequestVote = channel.unary_unary(
                '/raft.InternalRaftService/RequestVote',
                request_serializer=raft__pb2.VoteRequest.SerializeToString,
                response_deserializer=raft__pb2.VoteResponse.FromString,
                )


class InternalRaftServiceServicer(object):
    """Service for Raft internal operations
    """

    def AppendEntries(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RequestVote(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_InternalRaftServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'AppendEntries': grpc.unary_unary_rpc_method_handler(
                    servicer.AppendEntries,
                    request_deserializer=raft__pb2.EntryRequest.FromString,
                    response_serializer=raft__pb2.EntryResponse.SerializeToString,
            ),
            'RequestVote': grpc.unary_unary_rpc_method_handler(
                    servicer.RequestVote,
                    request_deserializer=raft__pb2.VoteRequest.FromString,
                    response_serializer=raft__pb2.VoteResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'raft.InternalRaftService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class InternalRaftService(object):
    """Service for Raft internal operations
    """

    @staticmethod
    def AppendEntries(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/raft.InternalRaftService/AppendEntries',
            raft__pb2.EntryRequest.SerializeToString,
            raft__pb2.EntryResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RequestVote(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/raft.InternalRaftService/RequestVote',
            raft__pb2.VoteRequest.SerializeToString,
            raft__pb2.VoteResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
