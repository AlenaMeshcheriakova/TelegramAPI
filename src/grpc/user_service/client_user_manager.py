from typing import Optional

import grpc
from src.grpc.user_service import user_service_pb2_grpc

class GRPCClientUserManager:
    """
    A class to manage a gRPC client connection and stub for communication with a gRPC server.
    """
    def __init__(self, server_address: str):
        """
        Initializes the GRPCClientUserManager with the server address.
        :param server_address: The address of the gRPC server to connect to.
        """
        self.server_address = server_address
        self.channel: Optional[grpc.Channel] = None
        self.stub: Optional[user_service_pb2_grpc.UserServiceGRPCStub] = None

    def _create_channel(self) -> grpc.Channel:
        """
        Creates and returns a gRPC channel if one does not already exist.
        """
        if self.channel is None:
            self.channel = grpc.insecure_channel(self.server_address)
        return self.channel

    def get_stub(self) -> user_service_pb2_grpc.UserServiceGRPCStub:
        """
        Returns the gRPC stub for calling server methods. Creates the stub if it does not already exist.
        :return: UserServiceGRPCStub - The gRPC stub for interacting with the server.
        """
        if self.stub is None:
            self.stub = user_service_pb2_grpc.UserServiceGRPCStub(self._create_channel())
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

    def __enter__(self) -> 'GRPCClientUserManager':
        """
        Enters the runtime context for the GRPCClientUserManager
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Exits the runtime context for the GRPCClientUserManager.
        """
        # Cleanup
        self.close()


def main():
    pass

if __name__ == '__main__':
    main()

