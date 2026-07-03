from fastapi import APIRouter, Response, Form, File, UploadFile
from pydantic.json_schema import SkipJsonSchema

from src.app.schemas.form import FormInfoDTO, InvestorFormInfoDTO, StartupFormInfoDTO
from infrastructure.db.enums import FormType, Currency

from src.services.form_service import FormServiceORM
from src.services.media_service import MediaServiceORM

router_form = APIRouter(prefix="/forms", tags=["Forms"])

@router_form.get("/", summary="получить список всех анкету", response_model=list[FormInfoDTO])
async def formslist():
    form_list = await FormServiceORM.show_all_forms()
    return form_list

@router_form.get("/{form_id}", summary="получить анкету", response_model=FormInfoDTO)
async def show_form(form_id: int):
    form = await FormServiceORM.show_one_form(form_id)
    return form

@router_form.get("/user/{user_id}", summary="получить список всех анкет пользователя", response_model=list[FormInfoDTO])
async def show_user_forms(user_id: int):
    result = await FormServiceORM.show_user_forms(user_id)
    return result

@router_form.post("/create", summary="создать анкету", response_model=FormInfoDTO)
async def create_form(
    user_id: int = Form(...),
    title: str = Form(...),
    description: str | None = Form(default=None),
    form_type: FormType = Form(...),
):
    form_info = FormInfoDTO(title=title, description=description, form_type=form_type)
    new_form = await FormServiceORM.new_form(user_id, form_info)
    return new_form

@router_form.post("/create/investor", summary="создать анкету инвестора", response_model=InvestorFormInfoDTO)
async def create_investor_form(
    user_id: int = Form(...),
    currency: Currency = Form(...),
    lowest_investment: float = Form(...),
    highest_investment: float = Form(...),
    royalty_percentage: float = Form(...),
):
    investor_info = InvestorFormInfoDTO(
        currency=currency,
        lowest_investment=lowest_investment,
        highest_investment=highest_investment,
        royalty_percentage=royalty_percentage
    )
    new_investor_form = await FormServiceORM.new_investor_info(user_id, investor_info)
    return new_investor_form

@router_form.post("/create/startup", summary="создать анкету стартапа", response_model=StartupFormInfoDTO)
async def create_startup_form(
    user_id: int = Form(...),
    currency: Currency = Form(...),
    required_investment: float = Form(...),
):
    startup_info = StartupFormInfoDTO(
        currency=currency,
        required_investment=required_investment
    )
    new_startup_form = await FormServiceORM.new_startup_info(user_id, startup_info)
    return new_startup_form

@router_form.put("/{form_id}/edit", summary="изменить анкету", response_model=FormInfoDTO)
async def edit_form(
    form_id: int,
    user_id: int = Form(...),
    title: str = Form(...),
    description: str | None = Form(default=None),
    form_type: FormType = Form(...),
):
    form_info = FormInfoDTO(title=title, description=description, form_type=form_type)
    edited_form = await FormServiceORM.change_form(user_id, form_id, form_info)
    return edited_form

@router_form.put("/{form_id}/edit/investor", summary="изменить анкету инвестора", response_model=InvestorFormInfoDTO)
async def edit_investor_form(
    form_id: int,
    user_id: int = Form(...),
    currency: Currency = Form(...),
    lowest_investment: float = Form(...),
    highest_investment: float = Form(...),
    royalty_percentage: float = Form(...),
):
    investor_info = InvestorFormInfoDTO(
        currency=currency,
        lowest_investment=lowest_investment,
        highest_investment=highest_investment,
        royalty_percentage=royalty_percentage
    )
    edited_investor_form = await FormServiceORM.change_investor_info(user_id, form_id, investor_info)
    return edited_investor_form

@router_form.put("/{form_id}/edit/startup", summary="изменить анкету стартапа", response_model=StartupFormInfoDTO)
async def edit_startup_form(
    form_id: int,
    user_id: int = Form(...),
    currency: Currency = Form(...),
    required_investment: float = Form(...),
):
    startup_info = StartupFormInfoDTO(
        currency=currency,
        required_investment=required_investment
    )
    edited_startup_form = await FormServiceORM.change_startup_info(user_id, form_id, startup_info)
    return edited_startup_form

@router_form.delete("/{form_id}/delete", summary="удалить анкету")
async def delete_form(form_id: int, user_id: int = Form(...)):
    await FormServiceORM.delete_form(user_id, form_id)
    return Response(status_code=204)

@router_form.post("/{form_id}/media", summary="добавить фото/видео к анкете")
async def upload_form_media(
    form_id: int,
    user_id: int = Form(...),
    media_files: list[UploadFile | SkipJsonSchema[str]] = File(...),
):
    files = MediaServiceORM.normalize_media_files(media_files)
    await MediaServiceORM.attach_media(user_id, form_id, files)
    return Response(status_code=204)

@router_form.delete("/{form_id}/media", summary="удалить все фото/видео анкеты")
async def delete_form_media(form_id: int, user_id: int = Form(...)):
    await MediaServiceORM.clear_form_media(user_id, form_id)
    return Response(status_code=204)