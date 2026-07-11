from fastapi import APIRouter

from src.app.schemas.doc import InnCheckDTO, VerificationResultDTO
from src.services.verification_service import VerificationServiceORM

router_doc = APIRouter(prefix="/verifications", tags=["Verifications"])

@router_doc.post("/egrul", summary="проверить компанию по ЕГРЮЛ/ЕГРИП", response_model=VerificationResultDTO)
async def check_egrul(data: InnCheckDTO):
    verification = await VerificationServiceORM.check_egrul(data.inn)
    return verification

@router_doc.post("/{company_id}/fssp", summary="проверить компанию по ФССП (исполнительные производства)", response_model=VerificationResultDTO)
async def check_fssp(company_id: int):
    verification = await VerificationServiceORM.check_fssp(company_id)
    return verification
