from datetime import date
from typing import Any, Optional
import sqlalchemy
from aiogram.fsm.context import FSMContext

from shared.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from shared.sqlalchemy_db_.sqlalchemy_model import UserDBM, DoctorPatientDBM, SurveyReminderDBM, SurveyResponseDBM
from tg_bot.handlers.common.message_service import MessageService
from tg_bot.handlers.patient.patient_survey_models import PatientSurvey


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
    

    @staticmethod
    async def survey_can_be_passed(
        state: FSMContext,
        message_id: int,
        notification_id: Optional[int] = None,
    ):
        if notification_id:
            patient_survey = PatientSurvey()
            success = await patient_survey.load(notification_id)
            if success:
                await MessageService.set_state_data(
                    state=state,
                    key=f"patient_survey:{message_id}",
                    value=patient_survey
                )
                return True
            return False
        else:
            patient_survey = await MessageService.get_state_data(
                state=state,
                key=f"patient_survey:{message_id}"
            )

            return bool(patient_survey)
        
    @staticmethod
    async def get_survey(
        state: FSMContext, 
        message_id: int, 
    ) -> PatientSurvey:
        return (await MessageService.get_state_data(
            state=state,
            key=f"patient_survey:{message_id}"
        ))
    
    @staticmethod
    async def save_modificate(
        state: FSMContext,
        message_id: int,
        modificated_survey: PatientSurvey
    ):
        await MessageService.set_state_data(
                state=state,
                key=f"patient_survey:{message_id}",
                value=modificated_survey
        )
    
    @staticmethod
    async def save_test_attemp(
        state: FSMContext,
        survey: PatientSurvey,
        message_id: int,
        patient_id: int
    ):
        await MessageService.set_state_data(
                state=state,
                key=f"patient_survey:{message_id}",
                value=None
        )
        
        async with get_cached_sqlalchemy_db().new_async_session() as async_session:
            # Получаем текущую попытку прохождения опроса
            curr_attemp = (await async_session.execute(
                sqlalchemy
                .select(SurveyReminderDBM)
                .where(SurveyReminderDBM.id == survey.notification_id)
            )).scalars().unique().one()
            
            schedule_date = date(curr_attemp.creation_dt.year, curr_attemp.creation_dt.month, curr_attemp.creation_dt.day)
            
            # Проверяем, есть ли уже завершенные или проваленные попытки 
            # для этого опроса и времени в тот же день
            existing_attempts = await async_session.execute(
                sqlalchemy
                .select(SurveyReminderDBM)
                .where(SurveyReminderDBM.scheduled_survey_id == survey.scheduled_survey_id)
                .where(SurveyReminderDBM.scheduled_time == survey.scheduled_time)
                .where(sqlalchemy.func.date(SurveyReminderDBM.creation_dt) == schedule_date)
                .where(SurveyReminderDBM.status.in_([
                    SurveyReminderDBM.ReminderStatus.COMPLETED,
                    SurveyReminderDBM.ReminderStatus.FAILED
                ]))
            )

            # Если такие попытки уже есть - просто выходим, ничего не меняя
            if existing_attempts.scalars().first() is not None:
                return False
            
            for number_question, answer in survey.answers.items():
                curr_question = survey.questions[number_question]
                survey_response = SurveyResponseDBM(
                    scheduled_survey_id=curr_attemp.scheduled_survey_id,
                    patient_id=patient_id,
                    question_id=curr_question.question_id,
                    answer=answer,
                    scheduled_time=curr_attemp.scheduled_time,
                )
                async_session.add(survey_response)
                await async_session.flush()

            # Помечаем текущую попытку как завершенную
            curr_attemp.status = SurveyReminderDBM.ReminderStatus.COMPLETED
            
                
            # Помечаем все другие ожидающие попытки для этого опроса 
            # и времени в тот же день как проваленные
            pending_attempts = await async_session.execute(
                sqlalchemy
                .select(SurveyReminderDBM)
                .where(SurveyReminderDBM.scheduled_survey_id == survey.scheduled_survey_id)
                .where(SurveyReminderDBM.scheduled_time == survey.scheduled_time)
                .where(sqlalchemy.func.date(SurveyReminderDBM.creation_dt) == schedule_date)
                .where(SurveyReminderDBM.id != survey.notification_id)
            )
            
            for attempt in pending_attempts.scalars():
                attempt.status = SurveyReminderDBM.ReminderStatus.FAILED
            
            await async_session.commit()
            
            return True