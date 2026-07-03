from datetime import date

from pydantic import BaseModel, Field, EmailStr, SecretStr
from infrastructure.db.enums import Role
from src.app.schemas.auth import TokenInfo

class UserIDDTO(BaseModel):
    id: int

class UserInfoDTO(BaseModel):
    name: str = Field(min_length=1, max_length=25, description="Максимально 25 символов.")
    surname: str = Field(min_length=1, max_length=25, description="Максимально 25 символов.")
    patronymic: str | None = Field(default=None)

class UserInfoRoleDTO(UserInfoDTO):
    role: Role

class UserCreateDTO(UserInfoDTO):
    email: EmailStr
    hashed_password: SecretStr

class UserExtrasDTO(UserInfoRoleDTO):
    is_active: bool

class UserFullInfoDTO(UserExtrasDTO, UserCreateDTO):
    pass

class UserInfoWithTokenDTO(BaseModel):
    user: UserFullInfoDTO
    token_info: TokenInfo | None = None