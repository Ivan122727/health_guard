from typing import Optional, List
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from shared.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from shared.sqlalchemy_db_.sqlalchemy_model import UserDBM
from tg_bot.handlers.common.message_service import MessageService


class PatientService(MessageService):
    """Сервис для работы с пациентами (Single Responsibility Principle)"""
    
    @classmethod
    async def get_available_doctors(
        cls,
    ) -> List[UserDBM]:
        """
        Получает список всех активных докторов
        
        Args:
            session: Опциональная сессия БД (для транзакций)
            
        Returns:
            List[UserDBM]: Список докторов
        """
        async with get_cached_sqlalchemy_db().new_async_session() as async_session:
            result = await async_session.execute(
                sqlalchemy.select(UserDBM)
                .where(
                    (UserDBM.role == UserDBM.Roles.doctor) &
                    (UserDBM.is_active == True)
                ))
            doctors = result.scalars().unique().all()
        
        return doctors

    @classmethod
    async def get_patient_doctors(
        cls,
        patient_id: int,
        session: Optional[AsyncSession] = None
    ) -> List[UserDBM]:
        """
        Получает список докторов пациента
        
        Args:
            patient_id: ID пациента в Telegram
            session: Опциональная сессия БД
            
        Returns:
            List[UserDBM]: Список докторов или пустой список
        """
        close_session = False
        if session is None:
            session = get_cached_sqlalchemy_db().new_async_session()
            close_session = True
            
        try:
            result = await session.execute(
                sqlalchemy.select(UserDBM)
                .where(UserDBM.tg_id == patient_id)
                .options(selectinload(UserDBM.doctor_relations))
            )
            patient = result.scalar_one_or_none()
            
            return patient.doctors if patient else []
        finally:
            if close_session:
                await session.close()
    
    @classmethod
    async def connect_to_doctor(
        cls,
        patient_id: int,
        doctor_id: int,
        session: Optional[AsyncSession] = None
    ) -> bool:
        """
        Связывает пациента с доктором
        
        Args:
            patient_id: ID пациента
            doctor_id: ID доктора
            session: Опциональная сессия БД
            
        Returns:
            bool: Успешность операции
        """
        from shared.sqlalchemy_db_.sqlalchemy_model import DoctorPatient
        
        close_session = False
        if session is None:
            session = get_cached_sqlalchemy_db().new_async_session()
            close_session = True
            
        try:
            # Проверяем существование связи
            existing = await session.execute(
                sqlalchemy.select(DoctorPatient)
                .where(
                    (DoctorPatient.patient_id == patient_id) &
                    (DoctorPatient.doctor_id == doctor_id))
            )
            
            if existing.scalar_one_or_none():
                return False  # Связь уже существует
                
            # Создаем новую связь
            new_relation = DoctorPatient(
                patient_id=patient_id,
                doctor_id=doctor_id
            )
            session.add(new_relation)
            await session.commit()
            
            return True
        except Exception:
            await session.rollback()
            return False
        finally:
            if close_session:
                await session.close()