import os
from pathlib import Path
from dotenv import load_dotenv

from pydantic import BaseModel
from pydantic_settings import BaseSettings

load_dotenv()

class DBSettings(BaseSettings):
    DB_HOST: str = str(os.getenv("DB_HOST"))
    DB_PORT: int = int(os.environ["DB_PORT"])
    DB_USER: str = str(os.getenv("DB_USER"))
    DB_PASS: str = str(os.getenv("DB_PASS"))
    DB_NAME: str = str(os.getenv("DB_NAME"))

    DB_MIGRATION_USER: str = str(os.getenv("DB_MIGRATION_USER"))
    DB_MIGRATION_PASS: str = str(os.getenv("DB_MIGRATION_PASS"))

    PASSPHRASE: bytes | None = (os.getenv("PASSPHRASE") or "").encode("utf-8") or None

    @property
    def DATABASE_URL_asyncpg(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    


BASE_DIR = Path(__file__).resolve().parent.parent
PRIVATE_KEY_PATH = BASE_DIR / "certs" / "private.pem"
PUBLIC_KEY_PATH = BASE_DIR / "certs" / "public.pem"

class AuthJWT(BaseModel):
    PRIVATE_KEY_PATH: Path = PRIVATE_KEY_PATH
    PUBLIC_KEY_PATH: Path = PUBLIC_KEY_PATH
    PASSPHRASE: bytes | None = (os.getenv("PASSPHRASE") or "").encode("utf-8") or None
    ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRATION_TIME_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRATION_TIME_DAYS: int = 30
    REFRESH_COOKIE_SECURE: bool = bool(os.getenv("REFRESH_COOKIE_SECURE"))

class MinIOSettings(BaseSettings):
    endpoint_url: str = str(os.getenv("S3_ENDPOINT"))
    access_key: str = str(os.getenv("S3_ACCESS_KEY"))
    secret_key: str = str(os.getenv("S3_SECRET_KEY"))
    bucket_name: str = str(os.getenv("S3_BUCKET"))

class Settings(BaseSettings):
    db: DBSettings = DBSettings()
    auth_jwt: AuthJWT = AuthJWT()
    minio: MinIOSettings = MinIOSettings()

settings = Settings()