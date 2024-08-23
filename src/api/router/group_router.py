from fastapi import APIRouter, Depends
from pydantic import UUID4

from src.api.auth.jwt_manager import JwtManager
from src.dto.schema import GroupAddDTO, GroupNameList, GroupUpdateDTO
from src.grpc.group_service.group_service import GroupService

router = APIRouter(
    prefix="/group",
    tags=["Group"]
)

@router.get("/groups")
def get_group(user_name: str, current_user: dict = Depends(JwtManager.get_current_user)):
    res = GroupService.get_groups_name_by_user_name(user_name)
    res_group_list = GroupNameList(group_names=res)
    return res_group_list


@router.post("/")
def add_group(group: GroupAddDTO, current_user: dict = Depends(JwtManager.get_current_user)):
    GroupService.create_group(group)
    return None

@router.put("/")
def update_group(group: GroupUpdateDTO, current_user: dict = Depends(JwtManager.get_current_user)):
    GroupService.update_group(group.id, group.new_group_name)
    return {"status": "success"}

@router.delete("/{group_id}")
def delete_group(group_id: UUID4, current_user: dict = Depends(JwtManager.get_current_user)):
    GroupService.delete_group(group_id)
    return {"status": "success"}
