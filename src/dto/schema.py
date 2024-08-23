import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, RootModel
from fastapi_users import schemas

class JWT_tocken(BaseModel):
    token: str
    expires_in: str

class UserResponse(BaseModel):
    username: str
    message: str

class RegisterRequest(BaseModel):
    username: str
    password: str
    email: EmailStr
    telegram_user_id: str

#---------------------User---------------------

class UserValidation(BaseModel):
    is_valid: bool
    user_id: uuid.UUID
    email: Optional[EmailStr] = None
    username: str = Field(max_length=35)

class UserDTO(schemas.BaseUser):
    # id: uuid.UUID
    user_name: str = Field(max_length=35)
    training_length: int = Field(ge=0)
    created_at: datetime
    updated_at: datetime

class UserDTOUpdate(schemas.BaseUser):
    user_name: str = Field(max_length=35)
    training_length: int = Field(ge=0)
    created_at: datetime
    updated_at: datetime

class UserCreateDTO(schemas.BaseUser):
    user_name: str = Field(max_length=35)
    training_length: int = Field(ge=0)

class UserCreateTelegramDTO(schemas.BaseUser):
    id: uuid.UUID
    user_name: str = Field(max_length=35)
    training_length: int = Field(ge=0)

class UserCreateFullDTO(schemas.BaseUser):
    id: uuid.UUID
    user_name: str = Field(max_length=35)
    training_length: int = Field(ge=0)
    created_at: datetime
    updated_at: datetime

#---------------------Word---------------------
class WordAddDTO(BaseModel):
    user_id: uuid.UUID
    german_word: str = Field(max_length=63)
    english_word: Optional[str] = Field(max_length=45)
    russian_word: Optional[str] = Field(max_length=33)
    amount_already_know: int = Field(ge=0)
    amount_back_to_learning: int = Field(ge=0)
    lang_level_id: uuid.UUID
    word_type_id: uuid.UUID
    group_id: uuid.UUID

class WordDTO(WordAddDTO):
    id: uuid.UUID

class WordGetDTO(BaseModel):
    user_id: uuid.UUID
    german_word: str = Field(max_length=63)
    english_word: Optional[str] = Field(max_length=45)
    russian_word: Optional[str] = Field(max_length=33)
    amount_already_know: int = Field(ge=0)
    amount_back_to_learning: int = Field(ge=0)
    lang_level_id: uuid.UUID
    word_type_id: uuid.UUID
    group_id: uuid.UUID

#---------------------StandardWordUser---------------------
class StandardWordAddDTO(BaseModel):
    user_id: uuid.UUID
    amount_already_know: int = Field(ge=0)
    amount_back_to_learning: int = Field(ge=0)
    word_id: uuid.UUID

class StandardWordDTO(StandardWordAddDTO):
    id: uuid.UUID

class StandardWordGetDTO(BaseModel):
    user_id: uuid.UUID
    amount_already_know: int = Field(ge=0)
    amount_back_to_learning: int = Field(ge=0)
    word_id: uuid.UUID


#---------------------Group---------------------
class GroupAddDTO(BaseModel):
    id: uuid.UUID
    group_name: str = Field(max_length=256)
    user_id: uuid.UUID

class GroupUpdateDTO(BaseModel):
    id: uuid.UUID
    new_group_name: str = Field(max_length=256)

class GroupDTO(GroupAddDTO):
    created_at: datetime
    updated_at: datetime

class GroupList(RootModel):
    root: List[GroupDTO]

class GroupNameList(BaseModel):
    group_names: List[str]

#---------------------Level---------------------

class LevelAddDTO(BaseModel):
    id: uuid.UUID = Field(max_length=256)
    lang_level: str

class LevelDTO(BaseModel):
    lang_level: str = Field(max_length=256)
    created_at: datetime
    updated_at: datetime

class LevelFullDTO(LevelAddDTO):
    created_at: datetime
    updated_at: datetime

class LevelUpdateDTO(BaseModel):
    id: uuid.UUID
    new_lang_level: str = Field(max_length=256)

class LevelList(RootModel):
    root: List[LevelDTO]

class LevelNameDTO(BaseModel):
    new_lang_level: str = Field(max_length=256)

#---------------------WordType---------------------

class WordTypeNameDTO(BaseModel):
    word_type: str = Field(max_length=256)

class WordTypeAddDTO(BaseModel):
    id: uuid.UUID
    word_type: str

class WordTypeDTO(BaseModel):
    word_type: str
    created_at: datetime
    updated_at: datetime

class WordTypeUpdateDTO(BaseModel):
    id: uuid.UUID
    word_type: str = Field(max_length=256)

class WordTypeList(RootModel):
    root: List[WordTypeDTO]
