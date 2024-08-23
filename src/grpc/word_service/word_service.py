import uuid
from typing import List

from cfg.сonfig import settings
from src.dto.schema import WordGetDTO, WordAddDTO
from src.grpc.mapping_helper import pydantic_to_protobuf, convert_proto_to_pydantic
from src.grpc.word_service import word_service_pb2
from src.grpc.word_service.client_word_manager import GRPCClientWordManager
from src.log.logger import CustomLogger, log_decorator
from src.model.level_enum import LevelEnum
from src.model.word_type_enum import WordTypeEnum

class WordService:

    server_address = settings.get_GRPC_conn

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def get_words_by_user(user_id: uuid.UUID, training_length: int = 10) -> List[WordGetDTO]:
        with GRPCClientWordManager(WordService.server_address) as word_manager:
            stub = word_manager.get_stub()
            request = word_service_pb2.GetWordsByUserRequest(
                user_id=str(user_id),
                training_length=training_length
            )
            response = stub.get_words_by_user(request)

            res_word_list = []
            for protobuff_word in response.words:
                dto_word = convert_proto_to_pydantic(protobuff_word, WordGetDTO)
                res_word_list.append(dto_word)
            return res_word_list

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def add_new_word_from_dto(word: WordAddDTO):
        with GRPCClientWordManager(WordService.server_address) as word_manager:
            stub = word_manager.get_stub()
            dto_mapping = {k: k for k, v in word.dict().items()}
            request = pydantic_to_protobuf(word, word_service_pb2.AddNewWordFromDtoRequest, dto_mapping)
            response = stub.add_new_word_from_dto(request)
            return response



    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def add_new_word(user_name: str, german_word: str, english_word: str, russian_word: str,
                     amount_already_know: int = 0, amount_back_to_learning: int = 0,
                     group_word_name: str = "CUSTOM_GROUP", level: LevelEnum = LevelEnum.a1,
                     word_type: WordTypeEnum = WordTypeEnum.custom) -> None:
        with GRPCClientWordManager(WordService.server_address) as word_manager:
            stub = word_manager.get_stub()
            request = word_service_pb2.AddNewWordRequest(
                user_name=user_name,
                german_word=german_word,
                english_word=english_word,
                russian_word=russian_word,
                amount_already_know=amount_already_know,
                amount_back_to_learning=amount_back_to_learning,
                group_word_name=group_word_name,
                level=level,
                word_type=word_type
            )

            response = stub.add_new_word(request)
            return response

def main():
    pass

if __name__ == '__main__':
    main()
