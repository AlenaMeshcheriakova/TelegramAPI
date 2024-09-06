import uuid

from cfg.сonfig import settings
from src.grpc.word_type_service import word_type_service_pb2
from src.grpc.word_type_service.client_word_type_manager import GRPCClientWordTypeManager
from src.log.logger import log_decorator, logger


class WordTypeService:

    server_address = settings.get_GRPC_conn

    @staticmethod
    @log_decorator(my_logger=logger)
    def get_word_type_id(wordType: str) -> uuid.UUID:
        """
        Get word type ID by wordType
        :param wordType: name of wordType
        :return: uuid for wordType
        """
        with GRPCClientWordTypeManager(WordTypeService.server_address) as word_type_manager:
            stub = word_type_manager.get_stub()
            request = word_type_service_pb2.GetWordTypeIdRequest(word_type=wordType)
            response = stub.get_word_type_id(request)
            word_type_uuid=uuid.UUID(response.word_type_id)
            return word_type_uuid

    @staticmethod
    @log_decorator(my_logger=logger)
    def create_word_type(wordType: str) -> uuid.UUID:
        """
        Create a new word type and return its UUID.
        """
        with GRPCClientWordTypeManager(WordTypeService.server_address) as word_type_manager:
            stub = word_type_manager.get_stub()
            request = word_type_service_pb2.CreateWordTypeRequest(word_type=wordType)
            response = stub.create_word_type(request)
            word_type_uuid = uuid.UUID(response.word_type_id)
            return word_type_uuid

    @staticmethod
    @log_decorator(my_logger=logger)
    def update_word_type(word_type_id: uuid.UUID, new_word_type: str) -> None:
        """
        Update the word type by its ID.
        """
        with GRPCClientWordTypeManager(WordTypeService.server_address) as word_type_manager:
            stub = word_type_manager.get_stub()
            request = word_type_service_pb2.UpdateWordTypeRequest(
                word_type_id=str(word_type_id),
                new_word_type=new_word_type
            )
            stub.update_word_type(request)
            return None

    @staticmethod
    @log_decorator(my_logger=logger)
    def delete_word_type(word_type_id: uuid.UUID) -> None:
        """
        Delete the word type by its ID and return success status.
        """
        with GRPCClientWordTypeManager(WordTypeService.server_address) as word_type_manager:
            stub = word_type_manager.get_stub()
            request = word_type_service_pb2.DeleteWordTypeRequest(word_type_id=str(word_type_id))
            stub.delete_word_type(request)
            return None