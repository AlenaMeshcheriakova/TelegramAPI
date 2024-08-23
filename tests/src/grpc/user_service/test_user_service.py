import datetime
import unittest
import uuid

import grpc
import pytest
from google.protobuf.internal.well_known_types import Timestamp

from src.dto.schema import UserCreateTelegramDTO, UserCreateFullDTO
from src.grpc.user_service import user_service_pb2_grpc, user_service_pb2
from src.grpc.user_service.user_service import UserService
from tests.src.grpc.user_service.mock_user_service import MockUserService, serve
from tests.src.test_data_preparation import DataPreparation

@pytest.fixture(scope='module')
def grpc_channel():
    import threading
    stop_event = threading.Event()
    server, wait_for_stop = serve(stop_event)

    yield grpc.insecure_channel('localhost:50051')

    stop_event.set()
    wait_for_stop()

@pytest.fixture
def grpc_stub(grpc_channel):
    return user_service_pb2_grpc.UserServiceGRPCStub(grpc_channel)

class TestUserService:

    def test_get_user_by_id(self, grpc_stub):
        user_id = str(DataPreparation.TEST_USER_ID)
        request = user_service_pb2.UserIdRequest(request_id=user_id)

        # Call the method under test
        response = grpc_stub.get_user_by_id(request)

        # Assert that the response is of the expected type
        assert isinstance(response, user_service_pb2.UserCreateFullDTOResponse)
        assert response.id == user_id
        assert response.user_name is not None

    def test_get_user_by_name(self, grpc_stub):
        user_name = DataPreparation.TEST_USER_NAME
        request = user_service_pb2.UserNameRequest(user_name=user_name)

        # Call the method under test
        response = grpc_stub.get_user_by_name(request)

        # Assert that the response is of the expected type
        assert isinstance(response, user_service_pb2.UserCreateFullDTOResponse)
        assert response.user_name == user_name
        assert response.email == DataPreparation.TEST_USER_EMAIL

    def test_get_user_id_by_name(self, grpc_stub):
        user_name = DataPreparation.TEST_USER_NAME
        request = user_service_pb2.UserNameRequest(user_name=user_name)

        # Call the method under test
        response = grpc_stub.get_user_id_by_name(request)

        # Assert that the response contains the expected UUID
        expected_uuid = DataPreparation.TEST_USER_ID
        assert uuid.UUID(response.user_id) == expected_uuid

    def test_create_user_by_DTO(self, grpc_stub):
        new_user = UserCreateTelegramDTO(
            user_name="new_user",
            training_length=10,
            telegram_user_id="telegram_123",
            hashed_password="hashed_password",
            email="new_user@example.com"
        )

        # Call the method under test
        grpc_stub.create_user_by_DTO(new_user)

        # No response is expected, so just check that no exceptions were raised
        assert True

    def test_create_user(self, grpc_stub):
        request = user_service_pb2.UserRequest(
            name="new_user",
            email="new_user@example.com",
            password="password123",
            training_length=10
        )

        # Call the method under test
        grpc_stub.create_user(request)

        # No response is expected, so just check that no exceptions were raised
        assert True

    def test_update_user_training_length(self, grpc_stub):
        user_name = DataPreparation.TEST_USER_NAME
        new_training_length = 20
        request = user_service_pb2.UserTrainingLengthRequest(
            user_name=user_name,
            training_length=new_training_length
        )

        # Call the method under test
        grpc_stub.update_user_training_length(request)

        # No response is expected, so just check that no exceptions were raised
        assert True

    def test_is_user_created(self, grpc_stub):
        user_name = DataPreparation.TEST_USER_NAME
        request = user_service_pb2.UserNameRequest(user_name=user_name)

        # Call the method under test
        response = grpc_stub.is_user_created(request)

        # Assert that the response contains the expected result
        assert response.result is True

    def test_create_user_by_parameters(self, grpc_stub):
        # Do tests
        UserService.create_user(DataPreparation.TEST_USER_NAME, DataPreparation.TEST_USER_EMAIL,
                                DataPreparation.TEST_PASS, DataPreparation.TEST_TELEGRAM_USER_ID, 10)

    def test_create_user_by_DTO(self, grpc_stub):
        # Prepare data
        test_user = UserCreateTelegramDTO(
            id=DataPreparation.TEST_USER_ID,
            user_name=DataPreparation.TEST_USER_NAME,
            telegram_user_id=DataPreparation.TEST_TELEGRAM_USER_ID,
            training_length=5,
            hashed_password=DataPreparation.TEST_PASS,
            email=DataPreparation.TEST_USER_EMAIL,
            is_active=True
        )

        # Do tests
        UserService.create_user_by_DTO(test_user)

    def test_get_user_by_name(self, grpc_stub):
        # Do tests
        test_user_name = UserService.get_user_by_name(DataPreparation.TEST_USER_NAME)

        assert test_user_name.telegram_user_id == str(DataPreparation.TEST_TELEGRAM_USER_ID)
        assert test_user_name.user_name == DataPreparation.TEST_USER_NAME
        assert test_user_name.email == DataPreparation.TEST_USER_EMAIL

    def test_get_user_by_id(self, grpc_stub):
        # Do tests
        test_user_name = UserService.get_user_by_id(DataPreparation.TEST_USER_ID)

        assert test_user_name.telegram_user_id == str(DataPreparation.TEST_TELEGRAM_USER_ID)
        assert test_user_name.user_name == DataPreparation.TEST_USER_NAME
        assert test_user_name.email == DataPreparation.TEST_USER_EMAIL

    def test_is_user_created_positive(self, grpc_stub):
        # Do tests
        is_user_created = UserService.is_user_created(DataPreparation.TEST_USER_NAME)

        assert is_user_created is True

    def test_is_user_created_negative(self, grpc_stub):
        # Do tests
        is_user_created = UserService.is_user_created("Fake user name")

        assert is_user_created is False

if __name__ == '__main__':
    unittest.main()
