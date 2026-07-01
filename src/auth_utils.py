from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt, jwt
from pydantic import SecretStr
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.backends import default_backend

from src.config import settings


class AuthUtils:
    @staticmethod
    def encode_jwt(
            payload: dict[str, Any],
            algorithm: str = settings.auth_jwt.ALGORITHM,
            expiration_minutes: int = settings.auth_jwt.ACCESS_TOKEN_EXPIRATION_TIME_MINUTES,
            expiration_timedelta: timedelta | None = None,
    ):
        to_encode = payload.copy()
        time_now = datetime.now(timezone.utc)
        if expiration_timedelta:
            expire_time = time_now + expiration_timedelta
        else:
            expire_time = time_now + timedelta(minutes=expiration_minutes)
        to_encode.update(exp=expire_time, iat=time_now)

        key = settings.auth_jwt.PRIVATE_KEY_PATH.read_text()
        raw_passphrase = settings.auth_jwt.PASSPHRASE
        if isinstance(raw_passphrase, str) and raw_passphrase and raw_passphrase != "None":
            password_bytes: bytes | None = raw_passphrase.encode("utf-8")
        elif isinstance(raw_passphrase, bytes):
            password_bytes = raw_passphrase
        else:
            password_bytes = None
        private_key = serialization.load_pem_private_key(
            key.encode("utf-8"), password=password_bytes, backend=default_backend()
        )

        if not isinstance(private_key, RSAPrivateKey):
            raise ValueError("The provided key is not a valid RSA private key.")

        encoded = jwt.encode(payload=to_encode, key=private_key, algorithm=algorithm)
        return encoded

    @staticmethod
    def decode_jwt(
            encoded: str | bytes,
            algorithm: str = settings.auth_jwt.ALGORITHM,
    ):
        public_key = settings.auth_jwt.PUBLIC_KEY_PATH.read_text()
        decoded = jwt.decode(jwt=encoded, key=public_key, algorithms=[algorithm])
        return decoded

    @staticmethod
    def hash_password(password: str | SecretStr):
        if isinstance(password, SecretStr):
            password = password.get_secret_value()
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def check_password(password: str | SecretStr, hashed_password: str):
        if isinstance(password, SecretStr):
            password = password.get_secret_value()
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
