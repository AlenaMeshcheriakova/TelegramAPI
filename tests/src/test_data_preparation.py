import uuid
from unittest.mock import MagicMock, patch
import pytest

from src.model.level_enum import LevelEnum
from src.model.word_type_enum import WordTypeEnum
from tests.conftest import client


# --------------------TEST CONSTANT--------------------
class DataPreparation:

    # Test user 1
    TEST_USER_ID = uuid.uuid4()
    TEST_USER_NAME = 'TEST_USER_NAME'
    TEST_USER_EMAIL = 'TEST_GRPC_USER_EMAIL@gmail.com'
    TEST_PASS = 'TEST_PASS'
    TEST_TELEGRAM_USER_ID = "12341234"

    # Test user 2
    TEST_USER_ID_2 = uuid.uuid4()
    TEST_USER_NAME_2 = 'TEST_USER_NAME2'
    TEST_USER_EMAIL_2 = 'TEST_GRPC_USER_EMAIL2@gmail.com'
    TEST_PASS_2 = 'TEST_PASS2'
    TEST_TELEGRAM_USER_ID_2 = "123412342"

    # Group
    TEST_GROUP_NAME = 'TEST_GROUP_NAME'
    TEST_GROUP_ID = uuid.uuid4()

    TEST_COMMON_GROUP_NAME = 'CUSTOM_GROUP'
    TEST_COMMON_GROUP_ID = uuid.uuid4()

    # Level
    TEST_LEVEL_NAME = LevelEnum.a1
    TEST_LEVEL_ID = uuid.uuid4()

    # Word type
    TEST_WORD_TYPE = WordTypeEnum.test
    TEST_CUSTOM_WORD_TYPE = WordTypeEnum.custom
    TEST_WORD_TYPE_ID = uuid.uuid4()
    TEST_CUSTOM_WORD_TYPE_ID = uuid.uuid4()

    # Word
    TEST_WORD_DICT = [
        {'german_word' : "Hallo",
         'english_word': "Hello",
         'russian_word': "Привет"},
        {'german_word': "beantragen",
         'english_word': "apply for",
         'russian_word': "предлагать"},
        {'german_word': "der Antrag",
         'english_word': "request",
         'russian_word': "Предложение"},
        {'german_word': "einzahlen",
         'english_word': "pay",
         'russian_word': "платить"},
        {'german_word': "die Einzahlung",
         'english_word': "Deposit",
         'russian_word': "взнос,оплата"},
        {'german_word': "verdienen",
         'english_word': "earn",
         'russian_word': "зарабатывать"},
        {'german_word': "überweisen",
         'english_word': "transfer",
         'russian_word': "переводить деньги"},
        {'german_word': "wechseln",
         'english_word': "change",
         'russian_word': "менять, обменивать"},
        {'german_word': "sperren",
         'english_word': "block, lock out",
         'russian_word': "закрывать,блокировать"},
        {'german_word': "der Wechsel",
         'english_word': "the change",
         'russian_word': "изменение"},
        {'german_word': "die überweisung",
         'english_word': "the transfer",
         'russian_word': "перевод денег"},
        {'german_word': "der Verdienst",
         'english_word': "income",
         'russian_word': "заработок, заслуга"}
    ]

    TEST_WORD_DICT_MINI = [
        {'german_word': "Hallo",
         'english_word': "Hello",
         'russian_word': "Привет"},
        {'german_word': "beantragen",
         'english_word': "apply for",
         'russian_word': "предлагать"},
        {'german_word': "der Antrag",
         'english_word': "request",
         'russian_word': "Предложение"}
    ]

    TEST_WORD = {'german_word': "Hallo",
         'english_word': "Hello",
         'russian_word': "Привет"}

# --------------------Mock--------------------

@pytest.fixture(scope="function")
@patch('src.grpc.auth_service.auth_service.AuthService.login')
def test_login( mock_login):
    # Setup mock response for AuthService.login
    mock_login.return_value = MagicMock(token="mock_token")

    client.post("/auth/login", params={
        "telegram_user_id": DataPreparation.TEST_USER_ID,
        "email": DataPreparation.TEST_USER_EMAIL,
        "username": DataPreparation.TEST_USER_NAME,
        "password": DataPreparation.TEST_PASS
    })
