from fastapi import HTTPException
from cfg.сonfig import settings
from src.dto.schema import UserValidation, JWT_tocken, UserResponse, RegisterRequest
from src.grpc.auth_service import auth_service_pb2
from src.grpc.auth_service.client_auth_manager import GRPCClientAuthManager
from src.grpc.mapping_helper import convert_proto_to_pydantic
from src.log.logger import log_decorator, logger

class AuthService:

    server_address = settings.get_AUTH_GRPC_conn

    @staticmethod
    @log_decorator(my_logger=logger)
    def validate_token(token: str) -> UserValidation:
        with GRPCClientAuthManager(AuthService.server_address) as auth_manager:
            stub = auth_manager.get_stub()
            request = auth_service_pb2.ValidateTokenRequest(token=token)
            response = stub.validate_token(request)
            if not response.is_valid:
                raise HTTPException(status_code=500, detail="Token verification failed")
            validated_user = convert_proto_to_pydantic(response, UserValidation)
            return validated_user

    @staticmethod
    @log_decorator(my_logger=logger)
    def login(username: str, password: str, email: str, telegram_user_id: str ) -> JWT_tocken:
        with GRPCClientAuthManager(AuthService.server_address) as auth_manager:
            stub = auth_manager.get_stub()
            request = auth_service_pb2.LoginRequest(
                username=username,
                password=password,
                email=email,
                telegram_user_id=telegram_user_id
            )
            response = stub.login(request)
            token = JWT_tocken(
                token=response.token,
                expires_in=response.expires_in
            )
            return token

    @staticmethod
    @log_decorator(my_logger=logger)
    def register(register_request: RegisterRequest) -> UserResponse:
        with GRPCClientAuthManager(AuthService.server_address) as auth_manager:
            stub = auth_manager.get_stub()
            request = auth_service_pb2.RegisterRequest(
                username=register_request.username,
                password=register_request.password,
                email=register_request.email,
                telegram_user_id=register_request.telegram_user_id
            )
            response = stub.register(request)
            response_message = UserResponse(
                username=response.username,
                message=response.message
            )
            return response_message
