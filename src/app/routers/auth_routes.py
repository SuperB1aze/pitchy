from fastapi import APIRouter, HTTPException, Response

from src.services.auth_service import AuthServiceORM
from src.app.schemas.auth import UserLogin, TokenInfo
from src.db.enums import Role
from src.services.auth_service import OptionalCredentials, RefreshCookie, RequiredUser

router_auth = APIRouter(tags=["Auth"])

@router_auth.post("/login", summary="login", response_model=TokenInfo)
async def user_auth(user: UserLogin, response: Response, credentials: OptionalCredentials):
    user_check = await AuthServiceORM.get_user_auth_status(credentials)
    if user_check is None or user_check.role == Role.ADMIN:
        checked_user = await AuthServiceORM.user_auth_validate(user.email, user.password)
        access_token = AuthServiceORM.create_access_token(checked_user)
        refresh_token = AuthServiceORM.create_refresh_token(checked_user)
        AuthServiceORM.set_refresh_cookie(response, refresh_token)
        return TokenInfo(
            access_token=access_token,
            token_type=AuthServiceORM.token_type,
        )
    
    raise HTTPException(status_code=403, detail="User is already authorized")

@router_auth.post("/refresh", summary="обновить access token", response_model=TokenInfo)
async def refresh_access_token(refresh_token: RefreshCookie = None):
    access_token = await AuthServiceORM.refresh_access_token(refresh_token)
    return TokenInfo(
        access_token=access_token,
        token_type=AuthServiceORM.token_type,
    )

@router_auth.get("/user-credentials", summary="данные о пользователе")
async def user_creds(user: RequiredUser):
    return {
        "email": user.email,
        "name": user.name,
        "surname": user.surname,
        "patronymic": user.patronymic,
        "role": user.role.value,
    }

@router_auth.post("/logout", summary="logout")
async def logout_user(response: Response):
    response.delete_cookie(key=AuthServiceORM.refresh_cookie_name)
    return {"detail": "Successfully logged out"}