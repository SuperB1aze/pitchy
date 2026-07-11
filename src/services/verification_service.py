from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.database import async_session_factory
from infrastructure.db.models import CompaniesOrm, VerificationsOrm
from infrastructure.db.enums import VerificationType, DocVerificationStatus
from src.infrastructure.verification.egrul import DaDataClient, DaDataError
from src.infrastructure.verification.fssp import DaMiaFsspClient, DaMiaError
from src.services.base_service import BaseServiceORM

PROVIDER_DADATA = "dadata"
PROVIDER_DAMIA = "damia"

# DaData party.state.status значения: ACTIVE, LIQUIDATING, LIQUIDATED, REORGANIZING, BANKRUPT
ACTIVE_PARTY_STATUSES = {"ACTIVE"}

# DaMIA (fssp/isps) Статусы: Завершено, Не завершено, Погашено
ACTIVE_FSSP_STATUS = "Не завершено"

class VerificationServiceORM(BaseServiceORM):
    model = VerificationsOrm
    not_found_detail = "Verification not found"

    @staticmethod
    async def _get_or_create_company(session: AsyncSession, inn: str) -> CompaniesOrm:
        company = await session.scalar(select(CompaniesOrm).where(CompaniesOrm.inn == inn))
        if company is not None:
            return company
        try:
            # SAVEPOINT so a unique-constraint race (two concurrent checks for
            # the same new INN) only rolls back this insert, not the whole session.
            async with session.begin_nested():
                company = CompaniesOrm(inn=inn)
                session.add(company)
                await session.flush()
        except IntegrityError:
            company = await session.scalar(select(CompaniesOrm).where(CompaniesOrm.inn == inn))
            if company is None:
                raise
        return company

    @staticmethod
    async def _get_or_create_verification(
        session: AsyncSession, company_id: int, verification_type: VerificationType
    ) -> VerificationsOrm:
        query = select(VerificationsOrm).where(
            VerificationsOrm.company_id == company_id,
            VerificationsOrm.type == verification_type,
        )
        verification = await session.scalar(query)
        if verification is not None:
            return verification
        try:
            async with session.begin_nested():
                verification = VerificationsOrm(company_id=company_id, type=verification_type)
                session.add(verification)
                await session.flush()
        except IntegrityError:
            verification = await session.scalar(query)
            if verification is None:
                raise
        return verification

    @staticmethod
    def _resolve_status(party: dict | None) -> DocVerificationStatus:
        if party is None:
            return DocVerificationStatus.FAILED
        party_status = (party.get("state") or {}).get("status")
        if party_status in ACTIVE_PARTY_STATUSES:
            return DocVerificationStatus.VERIFIED
        return DocVerificationStatus.FLAGGED

    @staticmethod
    def _extract_region(party: dict) -> str | None:
        address_data = ((party.get("address") or {}).get("data")) or {}
        kladr_id = address_data.get("region_kladr_id")
        if kladr_id and len(kladr_id) >= 2:
            return kladr_id[:2]
        return None

    @classmethod
    def _apply_party_to_company(cls, company: CompaniesOrm, party: dict) -> None:
        name_block = party.get("name") or {}
        company.ogrn = party.get("ogrn") or company.ogrn
        company.kpp = party.get("kpp") or company.kpp
        company.company_name = name_block.get("short_with_opf") or name_block.get("full_with_opf") or company.company_name
        company.region = cls._extract_region(party) or company.region

    @classmethod
    async def check_egrul(cls, inn: str) -> VerificationsOrm:
        client = DaDataClient(api_key=settings.dadata.api_key)
        try:
            response = await client.find_party(inn)
        except DaDataError as exc:
            raise HTTPException(status_code=502, detail=f"EGRUL provider error: {exc}") from exc

        suggestions = response.get("suggestions") or []
        party = suggestions[0].get("data") if suggestions else None
        status = cls._resolve_status(party)

        async with async_session_factory() as session:
            company = await cls._get_or_create_company(session, inn)
            if party:
                cls._apply_party_to_company(company, party)

            verification = await cls._get_or_create_verification(session, company.id, VerificationType.EGRUL)
            verification.provider = PROVIDER_DADATA
            verification.external_ref = party.get("hid") if party else None
            verification.status = status
            verification.result_json = response
            verification.checked_at = datetime.now(timezone.utc)

            await session.commit()
            await session.refresh(verification)
            return verification

    @staticmethod
    def _resolve_fssp_status(records: list[dict]) -> DocVerificationStatus:
        if not records:
            return DocVerificationStatus.VERIFIED
        if any(record.get("Статус") == ACTIVE_FSSP_STATUS for record in records):
            return DocVerificationStatus.FLAGGED
        return DocVerificationStatus.VERIFIED

    @classmethod
    async def check_fssp(cls, company_id: int) -> VerificationsOrm:
        async with async_session_factory() as session:
            company = await session.get(CompaniesOrm, company_id)
            if company is None:
                raise HTTPException(status_code=404, detail="Company not found")

            client = DaMiaFsspClient(api_key=settings.damia.api_key)
            try:
                records = await client.find_by_inn(company.inn)
            except DaMiaError as exc:
                raise HTTPException(status_code=502, detail=f"FSSP provider error: {exc}") from exc

            verification = await cls._get_or_create_verification(session, company.id, VerificationType.FSSP)
            verification.provider = PROVIDER_DAMIA
            verification.status = cls._resolve_fssp_status(records)
            verification.result_json = {"records": records}
            verification.checked_at = datetime.now(timezone.utc)

            await session.commit()
            await session.refresh(verification)
            return verification
