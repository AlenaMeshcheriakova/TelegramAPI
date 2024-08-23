import uuid
from typing import List
from uuid import UUID
from google.protobuf import empty_pb2

from cfg.сonfig import settings
from src.dto.schema import LevelDTO
from src.grpc.level_service import level_service_pb2
from src.grpc.level_service.client_level_manager import GRPCClientLevelManager
from src.log.logger import log_decorator, CustomLogger

class LevelService:
    server_address = settings.get_GRPC_conn

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def create_levels() -> None:
        with GRPCClientLevelManager(LevelService.server_address) as level_manager:
            stub = level_manager.get_stub()
            empty_request = empty_pb2.Empty()
            response = stub.create_levels(empty_request)
            return response

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def create_level(lang_level: str) -> None:
        with GRPCClientLevelManager(LevelService.server_address) as level_manager:
            stub = level_manager.get_stub()
            request = level_service_pb2.LevelRequest(
                level_enum=lang_level
            )
            stub.create_level(request)
            return None

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def get_levels() -> List[LevelDTO]:
        with GRPCClientLevelManager(LevelService.server_address) as level_manager:
            stub = level_manager.get_stub()
            empty_request = empty_pb2.Empty()
            response = stub.get_levels(empty_request)
            levels_list = response.levels
            levels = []
            for level_protobuf in levels_list:
                level_dto = LevelDTO(
                    lang_level=level_protobuf.lang_level,
                    created_at=level_protobuf.created_at.ToDatetime(),
                    updated_at=level_protobuf.updated_at.ToDatetime()
                )
                levels.append(level_dto)
            return levels

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def get_level_id_by_name(level_enum: str) -> UUID:
        with GRPCClientLevelManager(LevelService.server_address) as level_manager:
            stub = level_manager.get_stub()
            request = level_service_pb2.LevelRequest(
                level_enum=level_enum
            )
            response = stub.get_level_id_by_name(request)
            return uuid.UUID(response.id)

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def get_level_by_id(level_id: UUID) -> LevelDTO:
        with GRPCClientLevelManager(LevelService.server_address) as level_manager:
            stub = level_manager.get_stub()
            request = level_service_pb2.LevelIdRequest(level_id=str(level_id))
            response = stub.get_level_by_id(request)
            level_dto = LevelDTO(
                lang_level=response.lang_level,
                created_at=response.created_at.ToDatetime(),
                updated_at=response.updated_at.ToDatetime()
            )
            return level_dto

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def update_level(level_id: UUID, updated_level_name: str) -> None:
        with GRPCClientLevelManager(LevelService.server_address) as level_manager:
            stub = level_manager.get_stub()
            request = level_service_pb2.LevelUpdateRequest(
                level_id=str(level_id),
                updated_data=updated_level_name
            )
            response = stub.update_level(request)
            return response

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def delete_level(level_id: UUID) -> None:
        with GRPCClientLevelManager(LevelService.server_address) as level_manager:
            stub = level_manager.get_stub()
            request = level_service_pb2.LevelIdRequest(level_id=str(level_id))
            response = stub.delete_level(request)
            return response
