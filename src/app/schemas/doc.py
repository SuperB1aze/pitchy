from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from infrastructure.db.enums import VerificationType, DocVerificationStatus

class InnCheckDTO(BaseModel):
    inn: str = Field(description="ИНН юридического лица (10 цифр) или ИП (12 цифр)")

    @field_validator("inn")
    @classmethod
    def validate_inn(cls, value: str) -> str:
        if not value.isdigit() or len(value) not in (10, 12):
            raise ValueError("ИНН должен состоять из 10 или 12 цифр")
        return value

class VerificationResultDTO(BaseModel):
    id: int
    company_id: int
    type: VerificationType
    provider: str | None
    status: DocVerificationStatus
    result_json: dict | None
    checked_at: datetime

    model_config = {"from_attributes": True}
