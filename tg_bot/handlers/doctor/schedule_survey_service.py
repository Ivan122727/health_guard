from typing import Optional
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext

from shared.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from shared.sqlalchemy_db_.sqlalchemy_model import UserDBM, QuestionDBM, SurveyDBM, SurveyQuestionDBM
from tg_bot.handlers.common.message_service import MessageService
from tg_bot.handlers.doctor.survey_models import Question, ScheduledSurvey

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