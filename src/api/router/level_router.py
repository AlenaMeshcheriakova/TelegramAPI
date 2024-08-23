from fastapi import APIRouter, Depends
from pydantic import UUID4

from src.api.auth.jwt_manager import JwtManager
from src.dto.schema import LevelUpdateDTO, LevelNameDTO
from src.grpc.level_service.level_service import LevelService

router = APIRouter(
    prefix="/level",
    tags=["Level"]
)

@router.get("/levels")
def get_all_levels(current_user: dict = Depends(JwtManager.get_current_user)):
    res = LevelService.get_levels()
    return res

@router.post("/")
def create_level(level_name: LevelNameDTO, current_user: dict = Depends(JwtManager.get_current_user)):
    LevelService.create_level(level_name.new_lang_level)
    return {"message": "Level was created successfully"}

@router.get("/{level_id}")
def get_level_by_id(level_id: UUID4, current_user: dict = Depends(JwtManager.get_current_user)):
    level = LevelService.get_level_by_id(level_id)
    return level

@router.put("/")
def update_level(level: LevelUpdateDTO, current_user: dict = Depends(JwtManager.get_current_user)):
    LevelService.update_level(level.id, level.new_lang_level)
    return {"message": "Level updated successfully"}

@router.delete("/{level_id}")
def delete_level(level_id: UUID4, current_user: dict = Depends(JwtManager.get_current_user)):
    LevelService.delete_level(level_id)
    return {"message": "Level deleted successfully"}