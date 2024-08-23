from fastapi import APIRouter, Depends
from pydantic import UUID4

from src.api.auth.jwt_manager import JwtManager
from src.dto.schema import WordTypeUpdateDTO, WordTypeNameDTO
from src.grpc.word_type_service.word_type_service import WordTypeService

router = APIRouter(
    prefix="/wordType",
    tags=["WordType"]
)
@router.post("/")
def create_word_type(wordType: WordTypeNameDTO, current_user: dict = Depends(JwtManager.get_current_user)):
    res_uuid = WordTypeService.create_word_type(wordType.word_type)
    return {"status": f"WordType was created successfully with id {res_uuid}"}

@router.get("/{word_type_name}")
def get_word_type_id(word_type_name: str, current_user: dict = Depends(JwtManager.get_current_user)):
    res_uuid = WordTypeService.get_word_type_id(word_type_name)
    return {"status": f"WordType with name {word_type_name} exist with id {res_uuid}"}

@router.put("/{word_type_id}")
def update_word_type(wordType: WordTypeUpdateDTO, current_user: dict = Depends(JwtManager.get_current_user)):
    WordTypeService.update_word_type(wordType.id, wordType.word_type)
    return {"status": "success"}

@router.delete("/{word_type_id}")
def delete_word_type(word_type_id: UUID4, current_user: dict = Depends(JwtManager.get_current_user)):
    WordTypeService.delete_word_type(word_type_id)
    return {"status": "success"}