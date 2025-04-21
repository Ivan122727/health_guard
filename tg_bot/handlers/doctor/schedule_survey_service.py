from typing import Optional
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext
from datetime import date, time
from typing import Tuple

from shared.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from shared.sqlalchemy_db_.sqlalchemy_model import UserDBM, SurveyDBM, DoctorPatientDBM
from tg_bot.handlers.common.message_service import MessageService
from tg_bot.handlers.doctor.survey_models import Question, ScheduledSurvey
from tg_bot.utils.time_validator import TimeValidator
from tg_bot.utils.data_validator import DateValidator

class ScheduleSurveyService:
    @staticmethod
    async def _get_or_create_survey(
        state: FSMContext
    ) -> ScheduledSurvey:
        survey: ScheduledSurvey = await MessageService.get_state_data(
            state=state, key=ScheduledSurvey._STATE_KEY_SURVEY_DATA,
        )

        if survey is None:
            survey = ScheduledSurvey()
        
        return survey

    @staticmethod
    async def _save_survey_changes(
        state: FSMContext,
        survey: ScheduledSurvey
    ) -> None:
        await MessageService.set_state_data(
            state=state,
            key=ScheduledSurvey._STATE_KEY_SURVEY_DATA,
            value=survey,
        )

    @staticmethod
    async def clear_schedule_data(
        state: FSMContext,
    ):
        await MessageService.set_state_data(
            state=state,
            key=ScheduledSurvey._STATE_KEY_SURVEY_DATA,
            value=None,
        )

        await MessageService.set_state_data(
            state=state,
            key=ScheduledSurvey._STATE_KEY_SELECT_SURVEY_CURRENT_PAGE,
            value=None,
        )


    @staticmethod
    async def save_frequency_type_survey(
        state: FSMContext,
        frequency_type: str,
    ):
        survey = await ScheduleSurveyService._get_or_create_survey(state)

        survey.set_frequency_type(frequency_type)

        await ScheduleSurveyService._save_survey_changes(
            state=state,
            survey=survey,
        )
    
    @staticmethod
    async def set_times_per_day(
        state: FSMContext,
        times_per_day: Optional[int] = None,
    ):
        if times_per_day is None:
            return
        
        survey = await ScheduleSurveyService._get_or_create_survey(state)

        survey.set_times_per_day(times_per_day)

        await ScheduleSurveyService._save_survey_changes(
            state=state,
            survey=survey,
        )

    @staticmethod
    async def get_times_per_day(
        state: FSMContext,
    ):
        survey = await ScheduleSurveyService._get_or_create_survey(state)

        return survey.survey.times_per_day
    

    @staticmethod
    async def set_interval_days(
        state: FSMContext,
        interval_days: Optional[int] = None,
    ):
        if interval_days is None:
            return
        
        survey = await ScheduleSurveyService._get_or_create_survey(state)

        survey.set_interval_days(interval_days)

        await ScheduleSurveyService._save_survey_changes(
            state=state,
            survey=survey,
        )
    
    @staticmethod
    async def get_interval_days(
        state: FSMContext,
    ):
        survey = await ScheduleSurveyService._get_or_create_survey(state)

        return survey.survey.interval_days
    
    @staticmethod
    async def validate_and_parse_times(
        text: str,
        count: int,
        sorted: bool = True
    ) -> Tuple[bool, Optional[list[time]], Optional[str]]:
        return TimeValidator.validate_and_parse_times(text=text, count=count, sorted=sorted)

    @staticmethod
    async def save_times(
        state: FSMContext,
        schedule_times: list[time]
    ) -> None:
        survey = await ScheduleSurveyService._get_or_create_survey(state)

        survey.save_times(schedule_times=schedule_times)

        await ScheduleSurveyService._save_survey_changes(state, survey)

    
    @staticmethod
    async def validate_and_parse_survey_dates(
        start_date_str: Optional[str] = None,
        end_date_str: Optional[str] = None,
    ) -> Tuple[bool, Optional[date], Optional[date], Optional[str]]:
        return DateValidator.validate_survey_dates(
            start_date_str=start_date_str,
            end_date_str=end_date_str,
        )
    
    @staticmethod
    async def save_survey_period(
        state: FSMContext,
        start_date: date,
        end_date: date,
    ):
        survey = await ScheduleSurveyService._get_or_create_survey(state)

        survey.save_survey_period(
            start_date=start_date,
            end_date=end_date,
        )

        await ScheduleSurveyService._save_survey_changes(
            state=state,
            survey=survey,
        )
    
    @staticmethod
    async def get_available_surveys(
        user_id: int,
    ):
        async with get_cached_sqlalchemy_db().new_async_session() as session:
            survey_dbms = (await session.execute(
                sqlalchemy
                .select(SurveyDBM)
                .where(SurveyDBM.created_by == user_id)
                .where(SurveyDBM.is_active)
            )).scalars().unique().all()

        return survey_dbms

    @staticmethod
    async def save_select_survey_current_page(
        state: FSMContext,
        page: int
    ) -> None:
        await MessageService.set_state_data(
            state=state,
            key=ScheduledSurvey._STATE_KEY_SELECT_SURVEY_CURRENT_PAGE,
            value=page,
        )
    
    @staticmethod
    async def get_select_survey_current_page(
        state: FSMContext,
    ) -> Optional[int]:
        current_page = await MessageService.get_state_data(
            state=state,
            key=ScheduledSurvey._STATE_KEY_SELECT_SURVEY_CURRENT_PAGE,
        )
        
        if current_page is not None:
            return current_page
        
        return None 

    @staticmethod
    async def save_current_selected_survey(
        state: FSMContext,
        survey_id: int,
        user_id: int,
    ) -> None:
        async with get_cached_sqlalchemy_db().new_async_session() as session:
            survey_dbm = (await session.execute(
                sqlalchemy
                .select(SurveyDBM)
                .where(SurveyDBM.id == survey_id)
                .where(SurveyDBM.created_by == user_id)
            )).scalar_one_or_none()
        
        if survey_dbm:
            await MessageService.set_state_data(
                state=state,
                key=ScheduledSurvey._STATE_KEY_CURRENT_SELECTED_SURVEY,
                value=survey_dbm,
            )
    
    @staticmethod
    async def get_current_selected_survey(
        state: FSMContext,
    ) -> Optional[SurveyDBM]:
        survey_dbm = await MessageService.get_state_data(
            state=state,
            key=ScheduledSurvey._STATE_KEY_CURRENT_SELECTED_SURVEY,
        )
        
        if survey_dbm:
            return survey_dbm
        
        return None 
    
    @staticmethod
    async def get_connected_patients(
        user_id: int,
    ) -> list[UserDBM]:
        async with get_cached_sqlalchemy_db().new_async_session() as session:
            patient_dbms = (await session.execute(
                sqlalchemy
                .select(UserDBM)
                .where(UserDBM.role == UserDBM.Roles.patient)
                .join(DoctorPatientDBM, sqlalchemy.and_(
                    DoctorPatientDBM.doctor_id == user_id,
                    DoctorPatientDBM.patient_id == UserDBM.tg_id
                    )
                )
                .order_by(UserDBM.id)
            )).scalars().unique().all()
        
        return patient_dbms
    
    @staticmethod
    async def save_select_patient_current_page(
        state: FSMContext,
        page: int
    ) -> None:
        await MessageService.set_state_data(
            state=state,
            key=ScheduledSurvey._STATE_KEY_SELECT_PATIENT_CURRENT_PAGE,
            value=page,
        )

    @staticmethod
    async def get_select_patient_current_page(
        state: FSMContext,
    ) -> Optional[int]:
        current_page = await MessageService.get_state_data(
            state=state,
            key=ScheduledSurvey._STATE_KEY_SELECT_PATIENT_CURRENT_PAGE,
        )
        
        if current_page is not None:
            return current_page
        
        return None 