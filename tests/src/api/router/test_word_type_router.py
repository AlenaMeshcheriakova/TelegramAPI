import uuid
from unittest.mock import patch

from pydantic import UUID4
from src.grpc.word_type_service.word_type_service import WordTypeService
from tests.conftest import client
from tests.src.test_data_preparation import DataPreparation


class TestWordTypeRouter:

    @patch('src.api.auth.jwt_manager.JwtManager.verify_token')
    @patch('src.api.auth.jwt_manager.JwtManager.get_current_user')
    def test_create_word_type(self, mock_verify_token, mock_get_current_user):
        # Mock token verification
        mock_verify_token.return_value = {
            "username": DataPreparation.TEST_USER_NAME,
            "email": DataPreparation.TEST_USER_EMAIL
        }
        mock_get_current_user.return_value = {
            "username": DataPreparation.TEST_USER_NAME,
            "email": DataPreparation.TEST_USER_EMAIL
        }

        # Mock WordTypeService behavior
        with patch.object(WordTypeService, 'create_word_type', return_value=uuid.uuid4()) as mock_service:
            word_type_data = "Noun"
            response = client.post(f"/wordType/", json={"word_type": word_type_data}, cookies={"access_token": "valid_token"})

            # Validate response
            assert response.status_code == 200
            assert "WordType was created successfully with id" in response.json()["status"]
            mock_service.assert_called_once_with(word_type_data)

    @patch('src.api.auth.jwt_manager.JwtManager.verify_token')
    @patch('src.api.auth.jwt_manager.JwtManager.get_current_user')
    def test_get_word_type_id(self, mock_verify_token, mock_get_current_user):
        # Mock token verification
        mock_verify_token.return_value = {
            "username": DataPreparation.TEST_USER_NAME,
            "email": DataPreparation.TEST_USER_EMAIL
        }
        mock_get_current_user.return_value = {
            "username": DataPreparation.TEST_USER_NAME,
            "email": DataPreparation.TEST_USER_EMAIL
        }

        # Mock WordTypeService behavior
        word_type_name = "Verb"
        mock_uuid = str(uuid.uuid4())
        with patch.object(WordTypeService, 'get_word_type_id', return_value=mock_uuid) as mock_service:
            response = client.get(f"/wordType/{word_type_name}", cookies={"access_token": "valid_token"})

            # Validate response
            assert response.status_code == 200
            assert response.json() == {"status": f"WordType with name {word_type_name} exist with id {mock_uuid}"}
            mock_service.assert_called_once_with(word_type_name)

    @patch('src.api.auth.jwt_manager.JwtManager.verify_token')
    @patch('src.api.auth.jwt_manager.JwtManager.get_current_user')
    def test_update_word_type(self, mock_verify_token, mock_get_current_user):
        # Mock token verification
        mock_verify_token.return_value = {
            "username": DataPreparation.TEST_USER_NAME,
            "email": DataPreparation.TEST_USER_EMAIL
        }
        mock_get_current_user.return_value = {
            "username": DataPreparation.TEST_USER_NAME,
            "email": DataPreparation.TEST_USER_EMAIL
        }

        # Mock WordTypeService behavior
        with patch.object(WordTypeService, 'update_word_type') as mock_service:
            word_type_data = {
                "id": str(uuid.uuid4()),
                "word_type": "UpdatedNoun"
            }
            response = client.put(f"/wordType/{word_type_data['id']}", json=word_type_data, cookies={"access_token": "valid_token"})

            # Validate response
            assert response.status_code == 200
            assert response.json() == {"status": "success"}
            mock_service.assert_called_once_with(UUID4(word_type_data['id']), word_type_data["word_type"])

    @patch('src.api.auth.jwt_manager.JwtManager.verify_token')
    @patch('src.api.auth.jwt_manager.JwtManager.get_current_user')
    def test_delete_word_type(self, mock_verify_token, mock_get_current_user):
        # Mock token verification
        mock_verify_token.return_value = {
            "username": DataPreparation.TEST_USER_NAME,
            "email": DataPreparation.TEST_USER_EMAIL
        }
        mock_get_current_user.return_value = {
            "username": DataPreparation.TEST_USER_NAME,
            "email": DataPreparation.TEST_USER_EMAIL
        }

        # Mock WordTypeService behavior
        with patch.object(WordTypeService, 'delete_word_type') as mock_service:
            word_type_id = str(uuid.uuid4())
            response = client.delete(f"/wordType/{word_type_id}", cookies={"access_token": "valid_token"})

            # Validate response
            assert response.status_code == 200
            assert response.json() == {"status": "success"}
            mock_service.assert_called_once_with(UUID4(word_type_id))