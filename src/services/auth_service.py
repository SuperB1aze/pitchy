from typing import Any, Annotated, TypeAlias
from datetime import timedelta

from fastapi import Form, Depends, HTTPException, Response, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import EmailStr, SecretStr
from jwt.exceptions import InvalidTokenError

from src.auth_utils import AuthUtils
from src.app.schemas.auth import UserLogin
from src.config import settings
from src.services.user_service import UserServiceORM
from src.db.models import UsersOrm

optional_bearer = HTTPBearer(auto_error=False)


class AuthServiceORM:
    refresh_cookie_name = "refresh_token"
    token_type = "Bearer"

    @staticmethod
    async def user_auth_validate(
        email: EmailStr = Form(),
        password: str | SecretStr = Form(),
    ):
        user = await UserServiceORM.show_profile_by_email(email)

        if not AuthUtils.check_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return user

    @staticmethod
    def create_access_token(user: UsersOrm):
        jwt_payload = {
            "sub": user.email,
            "type": "access",
        }
        return AuthUtils.encode_jwt(jwt_payload)

    @staticmethod
    def create_refresh_token(user: UsersOrm):
        jwt_payload = {
            "sub": user.email,
            "type": "refresh",
        }
        return AuthUtils.encode_jwt(
            jwt_payload,
            expiration_timedelta=timedelta(
                days=settings.auth_jwt.REFRESH_TOKEN_EXPIRATION_TIME_DAYS
            ),
        )

    @staticmethod
    def set_refresh_cookie(response: Response, refresh_token: str):
        response.set_cookie(
            key=AuthServiceORM.refresh_cookie_name,
            value=refresh_token,
            httponly=True,
            secure=settings.auth_jwt.REFRESH_COOKIE_SECURE,
            samesite="lax",
            max_age=60 * 60 * 24 * settings.auth_jwt.REFRESH_TOKEN_EXPIRATION_TIME_DAYS,
        )

    @classmethod
    async def user_auth_jwt(cls, user: UserLogin | UsersOrm, user_exists: bool):
        if user_exists:
            if not isinstance(user, UserLogin):
                raise HTTPException(status_code=400, detail="Invalid login data")
            checked_user = await AuthServiceORM.user_auth_validate(user.email, user.password)
        else:
            if not isinstance(user, UsersOrm):
                raise HTTPException(status_code=400, detail="Invalid user data")
            checked_user = user
        return cls.create_access_token(checked_user)

    @staticmethod
    async def get_token_payload(credentials: HTTPAuthorizationCredentials):
        token = credentials.credentials
        try:
            payload = AuthUtils.decode_jwt(encoded=token)
        except (InvalidTokenError, ValueError):
            raise HTTPException(status_code=401, detail="Invalid token")
        return payload

    @staticmethod
    async def get_user_auth_status(credentials: HTTPAuthorizationCredentials | None = Depends(optional_bearer)):
        if credentials is None:
            return None
        checked_payload = await AuthServiceORM.get_token_payload(credentials)
        token_type = checked_payload.get("type")
        if token_type != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user_email = checked_payload.get("sub")
        if not isinstance(user_email, str):
            raise HTTPException(status_code=401, detail="Invalid token")
        user = await UserServiceORM.show_profile_by_email(user_email)
        return user

    @classmethod
    async def refresh_access_token(cls, refresh_token: str | None):
        if refresh_token is None:
            raise HTTPException(status_code=401, detail="Refresh token missing")

        try:
            payload = AuthUtils.decode_jwt(refresh_token)
        except (InvalidTokenError, ValueError):
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        token_type = payload.get("type")
        if token_type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        user_email = payload.get("sub")
        if not isinstance(user_email, str):
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        user = await UserServiceORM.show_profile_by_email(user_email)
        return cls.create_access_token(user)


async def get_required_user(user: UsersOrm | None = Depends(AuthServiceORM.get_user_auth_status)):
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user


OptionalCredentials: TypeAlias = Annotated[
    HTTPAuthorizationCredentials | None,
    Depends(optional_bearer),
]
RefreshCookie: TypeAlias = Annotated[
    str | None,
    Cookie(alias=AuthServiceORM.refresh_cookie_name),
]
RequiredUser: TypeAlias = Annotated[
    UsersOrm,
    Depends(get_required_user),
]
