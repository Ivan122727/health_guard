from typing import Any
import sqlalchemy
from aiogram.fsm.context import FSMContext

from shared.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from shared.sqlalchemy_db_.sqlalchemy_model import UserDBM, DoctorPatientDBM
from tg_bot.handlers.common.message_service import MessageService


class PatientService:
    """Класс для обработки операций, связанных с пациентами"""
    @staticmethod
    async def get_available_doctors() -> list[UserDBM]:
        async with get_cached_sqlalchemy_db().new_async_session() as async_session:
            result = await async_session.execute(
                sqlalchemy
                .select(UserDBM)
                .where(UserDBM.role == UserDBM.Roles.doctor)
                .where(UserDBM.is_active).order_by(UserDBM.id)
            )
            doctors = result.scalars().unique() 

        return doctors.all()


    @staticmethod
    async def get_patient_doctors(user_id: int) -> list[UserDBM]:
        async with get_cached_sqlalchemy_db().new_async_session() as async_session:
            result = await async_session.execute(
                sqlalchemy
                .select(UserDBM)
                .join(DoctorPatientDBM, UserDBM.tg_id == DoctorPatientDBM.doctor_id)
                .where(DoctorPatientDBM.patient_id == user_id)
            )
            doctors = result.scalars().unique()  
        return doctors.all()
    

    @staticmethod
    async def connect_patient_to_doctor(
        user_id: int, doctor_id: int
    ) -> None:
        async with get_cached_sqlalchemy_db().new_async_session() as async_session:
            doctor_dbm = (await async_session.execute(
                sqlalchemy
                .select(UserDBM)
                .where(UserDBM.tg_id == doctor_id)
                .where(UserDBM.is_active)
                .where(UserDBM.role == UserDBM.Roles.doctor)
            )).scalar_one()

            patient_dbm = (await async_session.execute(
                sqlalchemy
                .select(UserDBM)
                .where(UserDBM.tg_id == user_id)
                .where(UserDBM.is_active)
                .where(UserDBM.role == UserDBM.Roles.patient)
            )).scalar_one()            

            patient_doctor_relation_dbm = DoctorPatientDBM(
                doctor=doctor_dbm,
                patient=patient_dbm
            )
            async_session.add(patient_doctor_relation_dbm)
            await async_session.commit()
            await async_session.refresh(patient_doctor_relation_dbm)


    @staticmethod
    async def is_patient_has_connected(user_id: int) -> bool:
        return len(await PatientService.get_patient_doctors(user_id))


    @staticmethod
    async def get_selected_doctor(doctor_id: int) -> UserDBM:
        async with get_cached_sqlalchemy_db().new_async_session() as async_session:
            doctor_dbm = (await async_session.execute(
                sqlalchemy
                .select(UserDBM)
                .where(UserDBM.tg_id == doctor_id)
                .where(UserDBM.is_active)
                .where(UserDBM.role == UserDBM.Roles.doctor)
            )).scalar_one()
        return doctor_dbm
    

    @staticmethod
    async def save_connect_to_doctor_current_page(
        state: FSMContext,
        page: int
    ):
        await MessageService.set_state_data(
            state=state,
            key="connect_to_doctor_page",
            value=page,
        )

        
    @staticmethod
    async def get_connect_to_doctor_current_page(state: FSMContext):
        data = await state.get_data()
        return data.get("connect_to_doctor_page", 0)
    

    @staticmethod
    async def save_selected_doctor(
        state: FSMContext,
        doctor_id: int,
    ):
        await MessageService.set_state_data(
            state=state,
            key="selected_doctor_id",
            value=doctor_id,
        )

    @staticmethod
    async def get_selected_from_state(state: FSMContext):
        doctor_id = await MessageService.get_state_data(
            state=state, key="selected_doctor_id"
        )
        return doctor_id