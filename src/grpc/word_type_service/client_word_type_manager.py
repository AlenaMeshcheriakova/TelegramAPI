from typing import Optional

import grpc
from src.grpc.word_type_service import word_type_service_pb2_grpc

class GRPCClientWordTypeManager:
    """
    A class to manage a gRPC client connection and stub for communication with a gRPC server.
    """

    def __init__(self, server_address: str):
        """
        Initializes the GRPCClientWordTypeManager with the server address.
        :param server_address: The address of the gRPC server to connect to.
        """
        self.server_address = server_address
        self.channel: Optional[grpc.Channel] = None
        self.stub: Optional[word_type_service_pb2_grpc.WordTypeServiceStub] = None

    def _create_channel(self) -> grpc.Channel:
        """
        Creates and returns a gRPC channel if one does not already exist.
        """
        if self.channel is None:
            self.channel = grpc.insecure_channel(self.server_address)
        return self.channel

    def get_stub(self) -> word_type_service_pb2_grpc.WordTypeServiceStub:
        """
        Returns the gRPC stub for calling server methods. Creates the stub if it does not already exist.
        :return: WordTypeServiceStub - The gRPC stub for interacting with the server.
        """
        if self.stub is None:
            self.stub = word_type_service_pb2_grpc.WordTypeServiceStub(self._create_channel())
        return self.stub

    def close(self) -> None:
        """
        Closes the gRPC channel and clears the stub. This method should be called to clean up resources.
        :return: None
        """
        if self.channel:
            self.channel.close()
            self.channel = None
            self.stub = None

    def __enter__(self) -> 'GRPCClientWordTypeManager':
        """
        Enters the runtime context for the GRPCClientWordTypeManager
        """
        # Open resources
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Exits the runtime context for the GRPCClientWordTypeManager.
        """
        # Cleanup
        self.close()