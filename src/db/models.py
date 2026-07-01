from decimal import Decimal

from pydantic import EmailStr

from src.db.base_model import Base, int_primary_key, created_at, updated_at
from src.db.enums import Currency, FormType, DocVerificationStatus, Role

from sqlalchemy import String, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

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

class FormsOrm(Base):
    __tablename__ = "forms"

    id: Mapped[int_primary_key]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    form_type: Mapped[FormType] = mapped_column(nullable=False)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    user: Mapped["UsersOrm"] = relationship(back_populates="forms")
    investor_form: Mapped["InvestorFormsOrm"] = relationship(back_populates="form")
    startup_form: Mapped["StartupFormsOrm"] = relationship(back_populates="form")
    medias: Mapped[list["MediasOrm"]] = relationship(back_populates="form")
    legal_docs: Mapped[list["LegalDocsOrm"]] = relationship(back_populates="form")

    repl_cols = ("id", "user_id", "form_type")

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

class LegalDocsOrm(Base):
    __tablename__ = "legal_docs"

    id: Mapped[int_primary_key]
    form_id: Mapped[int] = mapped_column(ForeignKey("forms.id"), nullable=False)
    status: Mapped[DocVerificationStatus] = mapped_column(nullable=False, server_default=text(f"'{DocVerificationStatus.PENDING.name}'"))
    filepath: Mapped[str] = mapped_column(String(255), nullable=False)
    uploaded_at: Mapped[created_at]
    processed_at: Mapped[updated_at]

    form: Mapped["FormsOrm"] = relationship(back_populates="legal_docs")
    repl_cols = ("id", "form_id", "status", "filepath", "uploaded_at", "processed_at")