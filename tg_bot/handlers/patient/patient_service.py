import sqlalchemy

from shared.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from shared.sqlalchemy_db_.sqlalchemy_model import UserDBM, DoctorPatientDBM


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
    ):
        async with get_cached_sqlalchemy_db().new_async_session() as async_session:
            patient_doctor_relation_dbm = DoctorPatientDBM(
                patient_id=user_id,
                doctor_id=doctor_id
            )
            
            async_session.add(patient_doctor_relation_dbm)
            async_session.commit()

    @staticmethod
    async def get_doctor_selection_page(raw_data: str) -> int:
        try:
            page = int(raw_data.split(":")[1])
        except (IndexError, ValueError):
            page = 0
        
        return page