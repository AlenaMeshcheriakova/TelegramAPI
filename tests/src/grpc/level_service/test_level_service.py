import unittest
from datetime import datetime
from uuid import UUID
import grpc
import pytest

from google.protobuf import empty_pb2
from src.dto.schema import LevelDTO
from src.grpc.level_service import level_service_pb2, level_service_pb2_grpc
from src.grpc.level_service.level_service import LevelService
from src.grpc.mapping_helper import convert_protobuf_level_enum_to_python_enum
from src.model.level_enum import LevelEnum
from tests.src.grpc.level_service.mock_level_service import serve

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
    return level_service_pb2_grpc.LevelServiceGRPCStub(grpc_channel)


class TestLevelService:
    """Group of Unit-Tests for class LevelService"""

    def test_create_levels(self, grpc_stub):
        empty_request = empty_pb2.Empty()

        # Call the method under test
        grpc_stub.create_levels(empty_request)

    def test_get_levels(self, grpc_stub):
        empty_request = empty_pb2.Empty()

        response = grpc_stub.get_levels(empty_request)

        # Check if the response contains the expected levels
        assert len(response.levels) > 0

        for level in response.levels:
            assert isinstance(level.lang_level, level_service_pb2.LevelEnum.ValueType)
            assert level.created_at.seconds > 0
            assert level.updated_at.seconds > 0

        # Verify conversion to LevelDTO
        for level_protobuff in response.levels:
            level_dto = LevelDTO(
                lang_level=LevelEnum(convert_protobuf_level_enum_to_python_enum(level_protobuff.lang_level)),
                created_at=level_protobuff.created_at.ToDatetime(),
                updated_at=level_protobuff.updated_at.ToDatetime()
            )
            assert isinstance(level_dto.lang_level, LevelEnum)
            assert isinstance(level_dto.created_at, datetime)
            assert isinstance(level_dto.updated_at, datetime)

    def test_get_level_id_by_name(self, grpc_stub):
        level_enum = level_service_pb2.LevelEnum.A1
        request = level_service_pb2.LevelRequest(level_enum=level_enum)

        response = grpc_stub.get_level_id_by_name(request)

        expected_uuid = UUID('123e4567-e89b-12d3-a456-426614174000')
        assert UUID(response.id) == expected_uuid

        # Test with another level
        level_enum = level_service_pb2.LevelEnum.A2
        request = level_service_pb2.LevelRequest(level_enum=level_enum)

        response = grpc_stub.get_level_id_by_name(request)

        expected_uuid = UUID('123e4567-e89b-12d3-a456-426614174001')
        assert UUID(response.id) == expected_uuid


    def test_get_level_id_by_name(self, grpc_stub):
        # Do tests
        level_id = LevelService.get_level_id_by_name(LevelEnum.a1)

        # Check results
        assert level_id is not None

    def test_get_levels(self, grpc_stub):
        # Do tests
        levels = LevelService.get_levels()

        # Check results
        assert len(levels) == 2
        for level in levels:
            assert level.lang_level in LevelEnum

if __name__ == '__main__':
    unittest.main()