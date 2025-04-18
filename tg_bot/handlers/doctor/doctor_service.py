import sqlalchemy

from shared.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from shared.sqlalchemy_db_.sqlalchemy_model import UserDBM
from tg_bot.handlers.patient.patient_service import PatientService

class DoctorService:
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
    async def get_number_from_callback_data(raw_data: str, num_position: int = 2) -> int:
        try:
            page = int(raw_data.split(":")[num_position - 1])
        except (IndexError, ValueError):
            page = 0
        
        return page