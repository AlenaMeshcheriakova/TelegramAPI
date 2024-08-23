import unittest
import uuid

import grpc
import pytest

from src.grpc.word_type_service import word_type_service_pb2_grpc, word_type_service_pb2
from src.grpc.word_type_service.word_type_service import WordTypeService
from src.model.word_type_enum import WordTypeEnum
from tests.src.grpc.word_type_service.mock_word_type_service import serve


@pytest.fixture(scope="module")
def grpc_channel():
    import threading
    stop_event = threading.Event()
    server, wait_for_stop = serve(stop_event)

    yield grpc.insecure_channel('localhost:50051')

    stop_event.set()
    wait_for_stop()


@pytest.fixture
def grpc_stub(grpc_channel):
    return word_type_service_pb2_grpc.WordTypeServiceStub(grpc_channel)

class TestWordTypeService:

    def test_get_word_type_id_test(self, grpc_stub):
        # Simulate BASIC word type enum
        request = word_type_service_pb2.GetWordTypeIdRequest(word_type=word_type_service_pb2.WordTypeEnum.TEST_WORD_TYPE)

        # Perform gRPC call
        response = grpc_stub.get_word_type_id(request)

        # Validate the UUID response
        expected_uuid = uuid.UUID('123e4567-e89b-12d3-a456-426614174000')
        assert uuid.UUID(response.word_type_id) == expected_uuid

    def test_get_word_type_id_custom(self, grpc_stub):
        # Simulate CUSTOM word type enum
        request = word_type_service_pb2.GetWordTypeIdRequest(word_type=word_type_service_pb2.WordTypeEnum.CUSTOM)

        # Perform gRPC call
        response = grpc_stub.get_word_type_id(request)

        # Validate the UUID response
        expected_uuid = uuid.UUID('123e4567-e89b-12d3-a456-426614174002')
        assert uuid.UUID(response.word_type_id) == expected_uuid

    def test_get_word_type_id_standard(self, grpc_stub):
        # Simulate STANDARD word type enum
        request = word_type_service_pb2.GetWordTypeIdRequest(word_type=word_type_service_pb2.WordTypeEnum.STANDARD)

        # Perform gRPC call
        response = grpc_stub.get_word_type_id(request)

        # Validate the UUID response
        expected_uuid = uuid.UUID('123e4567-e89b-12d3-a456-426614174001')
        assert uuid.UUID(response.word_type_id) == expected_uuid

    def test_get_word_type_id(self, grpc_stub):
        # Prepare data
        word_type = WordTypeEnum.standard

        # Do tests
        res = WordTypeService.get_word_type_id(word_type)

        # Check results
        assert res is not None

if __name__ == '__main__':
    unittest.main()