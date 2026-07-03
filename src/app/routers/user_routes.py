from fastapi import APIRouter, HTTPException, Response, Form
from pydantic import EmailStr

from src.app.schemas.user import UserCreateDTO, UserFullInfoDTO, UserInfoDTO, UserInfoRoleDTO, UserInfoWithTokenDTO
from src.app.schemas.auth import TokenInfo
from src.services.auth_service import OptionalCredentials, RequiredUser
from infrastructure.db.models import UsersOrm
from infrastructure.db.enums import Role

from src.services.user_service import UserServiceORM
from src.services.auth_service import AuthServiceORM

router_user = APIRouter(prefix="/users", tags=["Users"])

def user_info_dto(user: UsersOrm):
    return UserFullInfoDTO.model_validate(user, from_attributes=True)

@router_user.get("/", summary="получить список всех пользователей", response_model=list[UserFullInfoDTO])
async def userslist():
    user_list = await UserServiceORM.show_all_users()
    return user_list

@router_user.get("/{user_id}", summary="проверить профиль пользователя", response_model=UserFullInfoDTO)
async def show_profile(user_id: int):
    user = await UserServiceORM.show_profile(user_id)
    return user

@router_user.post("/create_user", summary="создать пользователя", response_model=UserInfoWithTokenDTO)
async def create_user(
    response: Response,
    credentials: OptionalCredentials,
    name: str,
    surname: str,
    patronymic: str | None,
    email: EmailStr,
    password: str,
    password_confirm: str,
):
    if password != password_confirm:
        raise HTTPException(status_code=422, detail="Passwords do not match")
    new_user = UserCreateDTO(
        name=name,
        surname=surname,
        patronymic=patronymic,
        email=email,
        hashed_password=password,
    )
    if credentials is None:
        created_user = await UserServiceORM.new_user(new_user)
        created_user = await UserServiceORM.show_profile(created_user.id)
        access_token = AuthServiceORM.create_access_token(created_user)
        refresh_token = AuthServiceORM.create_refresh_token(created_user)
        AuthServiceORM.set_refresh_cookie(response, refresh_token)
        return UserInfoWithTokenDTO(
             **created_user,
             token_info = TokenInfo(
                  access_token=access_token,
                  token_type=AuthServiceORM.token_type
             )
        )

    user = await AuthServiceORM.get_user_auth_status(credentials)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if user.role == Role.ADMIN:
        created_user = await UserServiceORM.new_user(new_user)
        created_user = await UserServiceORM.show_profile(created_user.id)
        return UserInfoWithTokenDTO(
             user=user_info_dto(created_user),
             token_info=None,
        )
    raise HTTPException(status_code=403, detail="Log out to create a new account")

@router_user.post("/create_superuser", summary="создать суперпользователя", response_model=UserFullInfoDTO)
async def create_superuser(
    current_user: RequiredUser,
    superuser_role: Role,
    name: str = Form(...),
    surname: str = Form(...),
    patronymic: str | None = Form(default=None),
    email: EmailStr = Form(...),
    password: str = Form(...),
):
    new_user = UserCreateDTO(
        name=name,
        surname=surname,
        patronymic=patronymic,
        email=email,
        hashed_password=password,
    )
    if current_user.role == Role.ADMIN:
        created_superuser = await UserServiceORM.new_superuser(new_user, superuser_role)
        created_superuser = await UserServiceORM.show_profile(created_superuser.id)
        return created_superuser
    raise HTTPException(status_code=403, detail="Not enough permissions")

@router_user.patch("/me/edit", summary="изменить свой профиль", response_model=UserInfoDTO)
async def edit_own_profile(
    current_user: RequiredUser,
    name: str = Form(...),
    surname: str = Form(...),
    patronymic: str | None = Form(default=None)
):
    edited_user_info = UserInfoDTO(name=name, surname=surname, patronymic=patronymic)
    edited_user = await UserServiceORM.edit_profile(current_user.id, edited_user_info)
    edited_user = await UserServiceORM.show_profile(current_user.id)
    return edited_user

@router_user.patch("/{user_id}/edit", summary="изменить профиль пользователя", response_model=UserInfoRoleDTO)
async def edit_profile(
    user_id: int,
    current_user: RequiredUser,
    name: str = Form(...),
    surname: str = Form(...),
    patronymic: str | None = Form(default=None),
    role: Role = Form(...),
):
    if current_user.role == Role.ADMIN:
        edited_user_info = UserInfoRoleDTO(name=name, surname=surname, patronymic=patronymic, role=role)
        edited_user = await UserServiceORM.edit_profile(user_id, edited_user_info)
        edited_user = await UserServiceORM.show_profile(user_id)
        return edited_user
    raise HTTPException(status_code=403, detail="Not enough permissions")

@router_user.patch("/{user_id}/restore-deleted-account", summary="восстановить аккаунт, который был мягко удален")
async def restore_deleted_account(user_id: int, current_user: RequiredUser):
    if current_user.role == Role.ADMIN:
        restored_user = await UserServiceORM.restore_account(user_id)
        return restored_user
    raise HTTPException(status_code=403, detail="Not enough permissions")

@router_user.delete("/me/delete-account", summary="удалить свой профиль")
async def delete_own_profile(response: Response, current_user: RequiredUser):
    deleted_user = await UserServiceORM.soft_delete_user(current_user.id)
    response.delete_cookie(key=AuthServiceORM.refresh_cookie_name)
    return deleted_user

@router_user.delete("/{user_id}/delete-account", summary="мягкое удаление определённого пользователя")
async def delete_user_soft(user_id: int, current_user: RequiredUser):
    if current_user.role == Role.ADMIN or current_user.id == user_id:
        deleted_user = await UserServiceORM.soft_delete_user(user_id)
        return deleted_user
    raise HTTPException(status_code=403, detail="Not enough permissions")

@router_user.delete("/{user_id}/hard-delete-account", summary="жесткое удаление определённого пользователя")
async def delete_user_hard(user_id: int, current_user: RequiredUser):
    if current_user.role == Role.ADMIN:
        deleted_user = await UserServiceORM.hard_delete_user(user_id)
        return deleted_user
    raise HTTPException(status_code=403, detail="Not enough permissions")