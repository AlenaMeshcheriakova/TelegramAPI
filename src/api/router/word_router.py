import uuid
from fastapi import APIRouter, Depends
from src.api.auth.jwt_manager import JwtManager
from src.dto.schema import WordAddDTO
from src.grpc.word_service.word_service import WordService

router = APIRouter(
    prefix="/word",
    tags=["Word"]
)

@router.get("/words")
def get_words(user_id: uuid.UUID, current_user: dict = Depends(JwtManager.get_current_user)):
    res = WordService.get_words_by_user(user_id)
    return res


@router.post("/")
def add_word(word: WordAddDTO, current_user: dict = Depends(JwtManager.get_current_user)):
    res = WordService.add_new_word_from_dto(WordAddDTO)
    return res
