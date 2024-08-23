import uuid
from datetime import datetime

import grpc
from concurrent import futures
from google.protobuf import empty_pb2, timestamp_pb2
from google.protobuf.timestamp_pb2 import Timestamp

from src.grpc.user_service.user_service_pb2_grpc import UserServiceGRPCStub
from src.grpc.user_service import user_service_pb2_grpc, user_service_pb2
from tests.src.test_data_preparation import DataPreparation


class MockUserService(user_service_pb2_grpc.UserServiceGRPCServicer):
    def __init__(self):
        self.users = {}
        self.user_ids = {}

        self._initialize_mock_data()

    def _initialize_mock_data(self):
        # Create a few sample users
        user1_id = str(DataPreparation.TEST_USER_ID)
        user2_id = str(DataPreparation.TEST_USER_ID_2)

        user1 = user_service_pb2.UserCreateFullDTOResponse(
            id=user1_id,
            user_name=DataPreparation.TEST_USER_NAME,
            training_length=10,
            created_at=Timestamp(seconds=int(datetime.utcnow().timestamp())),
            updated_at=Timestamp(seconds=int(datetime.utcnow().timestamp()))
        )

        user2 = user_service_pb2.UserCreateFullDTOResponse(
            id=user2_id,
            user_name=DataPreparation.TEST_USER_NAME_2,
            training_length=10,
            created_at=Timestamp(seconds=int(datetime.utcnow().timestamp())),
            updated_at=Timestamp(seconds=int(datetime.utcnow().timestamp()))
        )

        # Populate the dictionaries
        self.users[user1_id] = user1
        self.users[user2_id] = user2
        self.user_ids["mock_user1"] = user1_id
        self.user_ids["mock_user2"] = user2_id

    def get_user_by_id(self, request, context):
        user_id = request.request_id
        if user_id in self.users:
            return self.users[user_id]
        raise ValueError("User not found")

    def get_user_by_name(self, request, context):
        user_name = request.user_name
        for user in self.user_ids:
            if user_name == self.users.get(self.user_ids.get(user)).user_name:
                return self.users.get(self.user_ids.get(user))
        raise ValueError("User not found")

    def get_user_id_by_name(self, request, context):
        user_name = request.user_name
        for user in self.user_ids:
            if user_name == self.users.get(self.user_ids.get(user)).user_name:
                return user_service_pb2.UserIdResponse(user_id=self.users.get(self.user_ids.get(user)).id)
        raise ValueError("User not found")

    def update_user_training_length(self, request, context):
        user_name = request.user_name
        if user_name in self.user_ids:
            user_id = self.user_ids[user_name]
            user = self.users[user_id]
            # Update the user training length
            updated_user = user_service_pb2.UserCreateFullDTOResponse(
                id=user.id,
                user_name=user.user_name,
                training_length=request.training_length,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            self.users[user_id] = updated_user
            return empty_pb2.Empty()
        raise ValueError("User not found")

    def is_user_created(self, request, context):
        user_name = request.user_name
        return user_service_pb2.CheckResponse(result=user_name in self.user_ids)

    def create_user_by_DTO(self, request, context):
        user_id = str(uuid.uuid4())
        user = user_service_pb2.UserCreateFullDTOResponse(
            id=user_id,
            user_name=request.user_name,
            training_length=request.training_length,
            created_at=Timestamp(seconds=int(datetime.utcnow().timestamp())),
            updated_at=Timestamp(seconds=int(datetime.utcnow().timestamp()))
        )
        self.users[user_id] = user
        self.user_ids[request.user_name] = user_id
        return empty_pb2.Empty()

    def create_user(self, request, context):
        user_id = str(uuid.uuid4())
        user = user_service_pb2.UserCreateFullDTOResponse(
            id=user_id,
            user_name=request.name,
            training_length=request.training_length,
            created_at=Timestamp(seconds=int(datetime.utcnow().timestamp())),
            updated_at=Timestamp(seconds=int(datetime.utcnow().timestamp()))
        )
        self.users[user_id] = user
        self.user_ids[request.name] = user_id
        return empty_pb2.Empty()

def serve(stop_event):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_service_pb2_grpc.add_UserServiceGRPCServicer_to_server(MockUserService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()

    def wait_for_stop():
        stop_event.wait()
        server.stop(grace=None)

    return server, wait_for_stop

