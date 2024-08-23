import unittest
import uuid
from uuid import UUID

import grpc
import pytest
from google.protobuf import empty_pb2

from src.dto.schema import WordAddDTO
from src.grpc.word_service import word_service_pb2_grpc, word_service_pb2
from src.grpc.word_service.word_service import WordService
from src.model.level_enum import LevelEnum
from src.model.word_type_enum import WordTypeEnum
from tests.src.grpc.word_service.mock_word_service import serve
from tests.src.test_data_preparation import DataPreparation

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
    return word_service_pb2_grpc.WordServiceStub(grpc_channel)

class TestWordService:
    """Group of Unit-Tests for class WordService"""

    def test_get_words_by_user(self, grpc_stub):
        # Mock user_id and training_length
        user_id = UUID('123e4567-e89b-12d3-a456-426614174000')
        training_length = 10

        # Perform gRPC call
        request = word_service_pb2.GetWordsByUserRequest(
            user_id=str(user_id),
            training_length=training_length
        )
        response = grpc_stub.get_words_by_user(request)

        # Validate response
        assert len(response.words) > 0
        word = response.words[0]
        assert word.german_word == "Hallo"
        assert word.english_word == "Hello"
        assert word.russian_word == "Привет"
        assert word.lang_level_id == "A1"
        assert word.word_type_id == "custom"

    def test_add_new_word_from_dto(self, grpc_stub):
        # Mock request data
        word_dto_request = word_service_pb2.AddNewWordFromDtoRequest(
            user_id="123e4567-e89b-12d3-a456-426614174000",
            german_word="Hallo",
            english_word="Hello",
            russian_word="Привет",
            amount_already_know=0,
            amount_back_to_learning=0,
            lang_level_id="A1",
            word_type_id="custom",
            group_id="group1"
        )

        # Perform gRPC call
        response = grpc_stub.add_new_word_from_dto(word_dto_request)

        # Validate response (should be empty)
        assert isinstance(response, empty_pb2.Empty)

    def test_add_new_word(self, grpc_stub):
        # Mock request data
        word_request = word_service_pb2.AddNewWordRequest(
            user_name="test_user",
            german_word="Hallo",
            english_word="Hello",
            russian_word="Привет",
            amount_already_know=0,
            amount_back_to_learning=0,
            group_word_name="CUSTOM_GROUP",
            level="A1",
            word_type="custom"
        )

        # Perform gRPC call
        response = grpc_stub.add_new_word(word_request)

        # Validate response (should be empty)
        assert isinstance(response, empty_pb2.Empty)

    def test_get_words_by_user(self, grpc_stub):
        # Do tests
        user_id = DataPreparation.TEST_USER_ID
        word_set = WordService.get_words_by_user(user_id,10)

        # Check results
        assert len(word_set) == 1

    def test_add_new_word_from_dto(self, grpc_stub):
        # Prepare data
        word = DataPreparation.TEST_WORD
        tested_word=WordAddDTO(
            user_id="d268f7bd-2f7f-47b2-86e8-2bf9ca898b79",
            german_word=word.get('german_word'),
            english_word=word.get('english_word'),
            russian_word=word.get('russian_word'),
            amount_already_know=0,
            amount_back_to_learning=0,
            lang_level_id="2f74b3a2-3cc8-4bd9-a35b-146ff427c0a8",
            word_type_id="1038e8a7-9d2b-41e0-a3be-fb9139ac4c85",
            group_id="91d12346-f279-446c-a187-f172f2914915"
        )

        # Do tests
        WordService.add_new_word_from_dto(tested_word)

    def test_add_new_word(self, grpc_stub):
        # Prepare data
        word = DataPreparation.TEST_WORD

        # Do tests
        WordService.add_new_word(DataPreparation.TEST_USER_NAME,
                                 word.get('german_word'),
                                 word.get('english_word1'),
                                 word.get('russian_word1'),
                                 0,
                                 0,
                                 group_word_name=DataPreparation.TEST_GROUP_NAME,
                                 level=LevelEnum.a1,
                                 word_type=WordTypeEnum.standard)

if __name__ == '__main__':
    unittest.main()