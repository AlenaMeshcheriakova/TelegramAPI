import unittest
import uuid
from uuid import UUID
import grpc
import pytest

from src.dto.schema import GroupAddDTO
from src.grpc.group_service import group_service_pb2, group_service_pb2_grpc
from src.grpc.group_service.group_service import GroupService
from tests.src.grpc.group_service.mock_group_service import serve
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
    return group_service_pb2_grpc.GroupServiceStub(grpc_channel)

class TestGroupService:
    """Group of Unit-Tests for class GRPC GroupService"""
    def test_get_groups_name_by_user_name(self, grpc_stub):
        user_name = "test_user"
        request = group_service_pb2.GetGroupsNameByUserNameRequest(user_name=user_name)

        # Call the method under test
        response = grpc_stub.get_groups_name_by_user_name(request)

        # Verify the response
        expected_groups = ['group1', 'group2', 'group3']
        assert response.group_names == expected_groups

    def test_create_group(self, grpc_stub):
        new_group = group_service_pb2.GroupAddDTO(
            id="new_group_id",
            group_name="new_group",
            user_id="user_id"
        )

        request = group_service_pb2.CreateGroupRequest(new_group=new_group)

        # Call the method under test
        grpc_stub.create_group(request)

    def test_get_group_id_by_group_name(self, grpc_stub):
        group_name = "group1"
        request = group_service_pb2.GetGroupIdByGroupNameRequest(group_name=group_name)

        response = grpc_stub.get_group_id_by_group_name(request)

        expected_uuid = UUID('123e4567-e89b-12d3-a456-426614174000')
        assert UUID(response) == expected_uuid

    def test_is_group_created(self, grpc_stub):
        group_name = "group2"
        request = group_service_pb2.IsGroupCreatedRequest(group_name=group_name)

        response = grpc_stub.is_group_created(request)

        assert response.created is True

        # Test with a group name that does not exist
        group_name = "non_existing_group"
        request = group_service_pb2.IsGroupCreatedRequest(group_name=group_name)

        response = grpc_stub.is_group_created(request)

        assert response.created is False

    def test_create_group(self, grpc_stub):
        # Prepare data
        test_id = uuid.uuid4()
        group_dta = GroupAddDTO(
            id=test_id,
            group_name="grpc test group 2",
            user_id=uuid.UUID("c8117038-7efd-4ca9-b48d-b4698a6170ed")
        )

        # Do tests
        res = GroupService.create_group(group_dta)

        # Check results
        assert res == None

    def test_get_group_id_by_group_name(self, grpc_stub):
        # Do tests
        result = GroupService.get_group_id_by_group_name(DataPreparation.TEST_GROUP_NAME)

        # Check results
        assert result is not None
        expected_uuid = UUID('123e4567-e89b-12d3-a456-426614174000')
        assert UUID(result) == expected_uuid

    def test_get_groups_name_by_user_name(self, grpc_stub):
        # Do tests
        result = GroupService.get_groups_name_by_user_name(DataPreparation.TEST_USER_NAME)

        # Check results
        assert len(result) == 3
        expected_groups = ['group1', 'group2', 'group3']
        assert result == expected_groups

    def test_is_group_created(self, grpc_stub):
        # Do tests
        result = GroupService.is_group_created("group1")

        # Check results
        assert result is True

if __name__ == '__main__':
    unittest.main()