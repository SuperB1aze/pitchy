from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.database import async_session_factory
from infrastructure.db.models import FormsOrm, UsersOrm, CompaniesOrm, InvestorFormsOrm, StartupFormsOrm
from infrastructure.db.enums import Role
from src.app.schemas.form import FormInfoDTO, InvestorFormInfoDTO, StartupFormInfoDTO
from src.services.base_service import BaseServiceORM

class FormServiceORM(BaseServiceORM):
    model = FormsOrm
    not_found_detail = "Form not found"

    @classmethod
    def list_query(cls):
        return (
            select(FormsOrm)
            .join(UsersOrm)
            .where(UsersOrm.is_active == True)
            .options(joinedload(FormsOrm.user))
        )
    
    @classmethod
    def detail_query(cls, object_id: int):
        return (
            select(FormsOrm)
            .join(UsersOrm)
            .where(FormsOrm.id == object_id, UsersOrm.is_active == True)
            .options(joinedload(FormsOrm.user))
        )
    
    @classmethod
    async def show_all_forms(cls):
        async with async_session_factory() as session:
            return await cls.show_all(session)
        
    @classmethod
    async def show_one_form(cls, object_id: int):
        async with async_session_factory() as session:
            return await super().show_one(session, object_id)
    
    @staticmethod
    async def show_user_forms(user_id: int):
        async with async_session_factory() as session:
            result = await session.execute(
                select(FormsOrm)
                .where(FormsOrm.user_id == user_id)
                .options(joinedload(FormsOrm.user))
            )
            return result.scalars().all()
    
    @staticmethod
    async def new_form(user_id: int, company_id: int, data: FormInfoDTO):
        async with async_session_factory() as session:
            company = await session.get(CompaniesOrm, company_id)
            if not company:
                raise HTTPException(status_code=404, detail="Company not found")
            form = FormsOrm(
                user_id=user_id,
                company_id=company_id,
                title=data.title,
                description=data.description,
                form_type=data.form_type,
            )
            session.add(form)
            await session.commit()
            await session.refresh(form)
            return form

    @staticmethod
    async def new_investor_info(user_id: int, form_id: int, data: InvestorFormInfoDTO):
        async with async_session_factory() as session:
            form = await session.get(FormsOrm, form_id)
            if not form:
                raise HTTPException(status_code=404, detail="Form not found")
            if form.user_id != user_id:
                raise HTTPException(status_code=403, detail="You do not have permission to change this form")
            investor_form = InvestorFormsOrm(
                id=form_id,
                currency=data.currency,
                lowest_investment=data.lowest_investment,
                highest_investment=data.highest_investment,
                royalty_percentage=data.royalty_percentage,
            )
            session.add(investor_form)
            await session.commit()
            await session.refresh(investor_form)
            return investor_form

    @staticmethod
    async def new_startup_info(user_id: int, form_id: int, data: StartupFormInfoDTO):
        async with async_session_factory() as session:
            form = await session.get(FormsOrm, form_id)
            if not form:
                raise HTTPException(status_code=404, detail="Form not found")
            if form.user_id != user_id:
                raise HTTPException(status_code=403, detail="You do not have permission to change this form")
            startup_form = StartupFormsOrm(
                id=form_id,
                currency=data.currency,
                required_investment=data.required_investment,
            )
            session.add(startup_form)
            await session.commit()
            await session.refresh(startup_form)
            return startup_form
        
    @staticmethod
    async def change_form(user_id: int, form_id: int, data: FormInfoDTO):
        async with async_session_factory() as session:
            form = await session.get(FormsOrm, form_id)
            if not form:
                raise HTTPException(status_code=404, detail="Form not found")
            if form.user_id != user_id:
                raise HTTPException(status_code=403, detail="You do not have permission to change this form")
            form.title = data.title
            form.description = data.description
            form.form_type = data.form_type
            await session.commit()
            await session.refresh(form)
            return form
        
    @staticmethod
    async def change_investor_info(user_id: int, form_id: int, data: InvestorFormInfoDTO):
        async with async_session_factory() as session:
            investor_form = await session.get(InvestorFormsOrm, form_id)
            if not investor_form:
                raise HTTPException(status_code=404, detail="Investor form not found")
            if investor_form.form.user_id != user_id:
                raise HTTPException(status_code=403, detail="You do not have permission to change this investor form")
            investor_form.currency = data.currency
            investor_form.lowest_investment = data.lowest_investment
            investor_form.highest_investment = data.highest_investment
            investor_form.royalty_percentage = data.royalty_percentage
            await session.commit()
            await session.refresh(investor_form)
            return investor_form
        
    @staticmethod
    async def change_startup_info(user_id: int, form_id: int, data: StartupFormInfoDTO):
        async with async_session_factory() as session:
            startup_form = await session.get(StartupFormsOrm, form_id)
            if not startup_form:
                raise HTTPException(status_code=404, detail="Startup form not found")
            if startup_form.form.user_id != user_id:
                raise HTTPException(status_code=403, detail="You do not have permission to change this startup form")
            startup_form.currency = data.currency
            startup_form.required_investment = data.required_investment
            await session.commit()
            await session.refresh(startup_form)
            return startup_form
        
    @staticmethod
    async def delete_form(user_id: int, form_id: int):
        async with async_session_factory() as session:
            form = await session.get(FormsOrm, form_id)
            user = await session.get(UsersOrm, user_id)
            if not form:
                raise HTTPException(status_code=404, detail="Form not found")
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            if form.user_id != user_id and user.role != Role.ADMIN:
                raise HTTPException(status_code=403, detail="You do not have permission to delete this form")
            await session.delete(form)
            await session.commit()
            return {"detail": "Form deleted successfully"}