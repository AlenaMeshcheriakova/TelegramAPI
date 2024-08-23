from typing import List
from uuid import UUID

from cfg.сonfig import settings
from src.dto.schema import GroupAddDTO
from src.grpc.group_service import group_service_pb2
from src.grpc.group_service.client_group_manager import GRPCClientGroupManager
from src.log.logger import log_decorator, CustomLogger


class GroupService:

    server_address = settings.get_GRPC_conn

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def get_groups_name_by_user_name(user_name: str) -> List[str]:
        with GRPCClientGroupManager(GroupService.server_address) as group_manager:
            stub = group_manager.get_stub()
            request = group_service_pb2.GetGroupsNameByUserNameRequest(user_name=user_name)
            response = stub.get_groups_name_by_user_name(request)
            res_group_list=response.group_names
            return res_group_list


    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def create_group(new_group: GroupAddDTO) -> None:
        with GRPCClientGroupManager(GroupService.server_address) as group_manager:
            stub = group_manager.get_stub()
            protobuff_group = group_service_pb2.GroupAddDTO(
                id=str(new_group.id),
                group_name=new_group.group_name,
                user_id=str(new_group.user_id)
            )
            request = group_service_pb2.CreateGroupRequest(new_group=protobuff_group)
            stub.create_group(request)

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def get_group_id_by_group_name(group_name: str) -> UUID:
        with GRPCClientGroupManager(GroupService.server_address) as group_manager:
            stub = group_manager.get_stub()
            request = group_service_pb2.GetGroupIdByGroupNameRequest(group_name=group_name)
            response = stub.get_group_id_by_group_name(request)
            result_uuid = response.group_id
            return result_uuid

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def is_group_created(group_name: str) -> bool:
        with GRPCClientGroupManager(GroupService.server_address) as group_manager:
            stub = group_manager.get_stub()
            request = group_service_pb2.IsGroupCreatedRequest(group_name=group_name)
            response = stub.is_group_created(request)
            isGroupCreated = response.created
            return isGroupCreated

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def update_group(group_id: UUID, new_group_name: str) -> None:
        with GRPCClientGroupManager(GroupService.server_address) as group_manager:
            stub = group_manager.get_stub()
            request = group_service_pb2.UpdateGroupRequest(
                group_id=str(group_id),
                new_group_name=new_group_name
            )
            stub.update_group(request)

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def delete_group(group_id: UUID) -> None:
        with GRPCClientGroupManager(GroupService.server_address) as group_manager:
            stub = group_manager.get_stub()
            request = group_service_pb2.DeleteGroupRequest(group_id=str(group_id))
            stub.delete_group(request)