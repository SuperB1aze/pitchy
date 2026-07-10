from decimal import Decimal

from pydantic import EmailStr

from infrastructure.db.base_model import Base, int_primary_key, created_at, updated_at
from infrastructure.db.enums import Currency, FormType, DocVerificationStatus, Role, VerificationType

from sqlalchemy import String, ForeignKey, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int_primary_key]
    name: Mapped[str] = mapped_column(String(25), nullable=False)
    surname: Mapped[str] = mapped_column(String(25), nullable=False)
    patronymic: Mapped[str] = mapped_column(String(25))
    email: Mapped[EmailStr] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[Role]
    is_active: Mapped[bool] = mapped_column(nullable=False, server_default=text("true"))
    created_at: Mapped[created_at]

    forms: Mapped[list["FormsOrm"]] = relationship(back_populates="user")
    repl_cols = ("id", "email", "name", "surname", "role")

class CompaniesOrm(Base):
    __tablename__ = "companies"

    id: Mapped[int_primary_key]
    inn: Mapped[str] = mapped_column(String(12), unique=True, nullable=False)
    ogrn: Mapped[str | None] = mapped_column(String(15))
    company_name: Mapped[str | None] = mapped_column(String(255))
    region: Mapped[str | None] = mapped_column(String(3))
    kpp: Mapped[str | None] = mapped_column(String(9))

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    forms: Mapped[list["FormsOrm"]] = relationship(back_populates="company")
    verifications: Mapped[list["VerificationsOrm"]] = relationship(back_populates="company")

    repl_cols = ("id", "inn", "ogrn", "company_name")

class FormsOrm(Base):
    __tablename__ = "forms"

    id: Mapped[int_primary_key]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    form_type: Mapped[FormType] = mapped_column(nullable=False)

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    user: Mapped["UsersOrm"] = relationship(back_populates="forms")
    company: Mapped["CompaniesOrm"] = relationship(back_populates="forms")
    investor_form: Mapped["InvestorFormsOrm"] = relationship(back_populates="form")
    startup_form: Mapped["StartupFormsOrm"] = relationship(back_populates="form")
    medias: Mapped[list["MediasOrm"]] = relationship(back_populates="form")

    repl_cols = ("id", "user_id", "company_id", "form_type")

class InvestorFormsOrm(Base):
    __tablename__ = "investor_forms"

    id: Mapped[int_primary_key] = mapped_column(ForeignKey("forms.id"), primary_key=True)
    currency: Mapped[Currency] = mapped_column(nullable=False)
    lowest_investment: Mapped[int] = mapped_column(nullable=False)
    highest_investment: Mapped[int] = mapped_column(nullable=False)
    royalty_percentage: Mapped[Decimal] = mapped_column(nullable=False)

    form: Mapped["FormsOrm"] = relationship(back_populates="investor_form")
    repl_cols = ("id", "currency", "lowest_investment", "highest_investment", "royalty_percentage")

class StartupFormsOrm(Base):
    __tablename__ = "startup_forms"

    id: Mapped[int_primary_key] = mapped_column(ForeignKey("forms.id"), primary_key=True)
    currency: Mapped[Currency] = mapped_column(nullable=False)
    required_investment: Mapped[int] = mapped_column(nullable=False)

    form: Mapped["FormsOrm"] = relationship(back_populates="startup_form")
    repl_cols = ("id", "currency", "required_investment")

class MediasOrm(Base):
    __tablename__ = "medias"

    id: Mapped[int_primary_key]
    form_id: Mapped[int] = mapped_column(ForeignKey("forms.id"), nullable=False)
    filepath: Mapped[str] = mapped_column(String(255), nullable=False)
    uploaded_at: Mapped[created_at]

    form: Mapped["FormsOrm"] = relationship(back_populates="medias")
    repl_cols = ("id", "form_id", "filepath", "uploaded_at")

class VerificationsOrm(Base):
    __tablename__ = "verifications"

    id: Mapped[int_primary_key]
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)

    type: Mapped[VerificationType] = mapped_column(nullable=False)
    provider: Mapped[str | None] = mapped_column(String(50))
    external_ref: Mapped[str | None] = mapped_column(String(255))

    status: Mapped[DocVerificationStatus] = mapped_column(nullable=False, server_default=text(f"'{DocVerificationStatus.PENDING.name}'"))
    result_json: Mapped[dict | None] = mapped_column(JSONB)
    checked_at: Mapped[created_at]

    company: Mapped["CompaniesOrm"] = relationship(back_populates="verifications")

    __table_args__ = (
        UniqueConstraint("company_id", "type", name="uq_verification_company_type"),
    )
    repl_cols = ("id", "company_id", "type", "status", "checked_at")