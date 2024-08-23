import uuid
from unittest.mock import patch

from pydantic import UUID4

from src.grpc.word_service.word_service import WordService
from tests.conftest import client
from tests.src.test_data_preparation import DataPreparation


class TestWordRouter:

    @patch('src.api.auth.jwt_manager.JwtManager.verify_token')
    @patch('src.api.auth.jwt_manager.JwtManager.get_current_user')
    def test_get_words(self, mock_verify_token, mock_get_current_user):
        # Mock token verification
        mock_verify_token.return_value = {
            "username": DataPreparation.TEST_USER_NAME,
            "email": DataPreparation.TEST_USER_EMAIL
        }
        mock_get_current_user.return_value = {
            "username": DataPreparation.TEST_USER_NAME,
            "email": DataPreparation.TEST_USER_EMAIL
        }

        # Mock WordService behavior
        with patch.object(WordService, 'get_words_by_user', return_value=["Word1", "Word2"]) as mock_service:
            user_id = str(uuid.uuid4())
            response = client.get(f"/word/words?user_id={user_id}", cookies={"access_token": "valid_token"})

            # Validate response
            assert response.status_code == 200
            assert response.json() == ["Word1", "Word2"]
            mock_service.assert_called_once_with(UUID4(user_id))

    @patch('src.api.auth.jwt_manager.JwtManager.verify_token')
    @patch('src.api.auth.jwt_manager.JwtManager.get_current_user')
    def test_add_word(self, mock_verify_token, mock_get_current_user):
        # Mock token verification
        mock_verify_token.return_value = {
            "username": DataPreparation.TEST_USER_NAME,
            "email": DataPreparation.TEST_USER_EMAIL
        }
        mock_get_current_user.return_value = {
            "username": DataPreparation.TEST_USER_NAME,
            "email": DataPreparation.TEST_USER_EMAIL
        }

        # Mock WordService behavior
        with patch.object(WordService, 'add_new_word_from_dto', return_value={"message": "Word added successfully"}) as mock_service:
            word_data = {
                "user_id": str(uuid.uuid4()),
                "german_word": "Haus",
                "english_word": "House",
                "russian_word": "Дом",
                "amount_already_know": 5,
                "amount_back_to_learning": 2,
                "lang_level_id": str(uuid.uuid4()),
                "word_type_id": str(uuid.uuid4()),
                "group_id": str(uuid.uuid4())
            }

            response = client.post("/word/", json=word_data, cookies={"access_token": "valid_token"})

            # Validate response
            assert response.status_code == 200
            assert response.json() == {"message": "Word added successfully"}
            mock_service.assert_called_once()