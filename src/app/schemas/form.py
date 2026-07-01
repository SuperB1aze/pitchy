from decimal import Decimal

from pydantic import BaseModel, Field
from src.db.enums import FormType, Currency

class FormInfoDTO(BaseModel):
    title: str = Field(max_length=50, description="Максимально 50 символов.")
    description: str | None = Field(default=None, max_length=500, description="Максимально 500 символов.")
    form_type: FormType = Field(description="Тип формы")

class InvestorFormInfoDTO(BaseModel):
    currency: Currency = Field(description="Валюта")
    lowest_investment: int = Field(gt=0, description="Минимальная сумма инвестиций")
    highest_investment: int = Field(gt=0, description="Максимальная сумма инвестиций")
    royalty_percentage: Decimal = Field(gt=0, description="Процент роялти")

class StartupFormInfoDTO(BaseModel):
    currency: Currency = Field(description="Валюта")
    required_investment: int = Field(gt=0, description="Необходимая сумма инвестиций")