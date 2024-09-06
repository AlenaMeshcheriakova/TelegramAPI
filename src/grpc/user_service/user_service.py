import uuid

from cfg.сonfig import settings
from src.dto.schema import  UserCreateFullDTO
from src.grpc.mapping_helper import convert_proto_to_pydantic
from src.grpc.user_service import user_service_pb2
from src.grpc.user_service.client_user_manager import GRPCClientUserManager
from src.log.logger import log_decorator, logger

class UserService:

    server_address = settings.get_GRPC_conn

    @staticmethod
    @log_decorator(my_logger=logger)
    def get_user_by_id(user_id: uuid.UUID) -> UserCreateFullDTO:
        with GRPCClientUserManager(UserService.server_address) as user_manager:
            stub = user_manager.get_stub()
            request = user_service_pb2.UserIdRequest(
                request_id=str(user_id)
            )
            response = stub.get_user_by_id(request)
            dto = convert_proto_to_pydantic(response, UserCreateFullDTO)
            return dto

    @staticmethod
    @log_decorator(my_logger=logger)
    def get_user_by_name(user_name: str) -> UserCreateFullDTO:
        with GRPCClientUserManager(UserService.server_address) as user_manager:
            stub = user_manager.get_stub()
            request = user_service_pb2.UserNameRequest(
                user_name=user_name
            )
            response = stub.get_user_by_name(request)
            dto = convert_proto_to_pydantic(response, UserCreateFullDTO)
            return dto

    @staticmethod
    @log_decorator(my_logger=logger)
    def get_user_id_by_name(user_name: str) -> uuid.UUID:
        with GRPCClientUserManager(UserService.server_address) as user_manager:
            stub = user_manager.get_stub()
            request = user_service_pb2.UserNameRequest(
                user_name=user_name
            )
            response = stub.get_user_id_by_name(request)
            return response.user_id

    @staticmethod
    @log_decorator(my_logger=logger)
    def update_user_training_length(user_name: str, new_training_length: int) -> None:
        with GRPCClientUserManager(UserService.server_address) as user_manager:
            stub = user_manager.get_stub()
            request = user_service_pb2.UserTrainingLengthRequest(
                user_name=user_name,
                training_length=new_training_length
            )
            stub.update_user_training_length(request)

    @staticmethod
    @log_decorator(my_logger=logger)
    def is_user_created(user_name: str) -> bool:
        with GRPCClientUserManager(UserService.server_address) as user_manager:
            stub = user_manager.get_stub()
            request = user_service_pb2.UserNameRequest(
                user_name=user_name
            )
            response = stub.is_user_created(request)
            return response.result

def main():
    pass

if __name__ == '__main__':
    main()
