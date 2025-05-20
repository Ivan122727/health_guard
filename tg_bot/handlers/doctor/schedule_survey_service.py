from typing import Any, Optional
import sqlalchemy
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext
from datetime import date, datetime, time, timedelta
from typing import Tuple

from shared.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from shared.sqlalchemy_db_.sqlalchemy_model import UserDBM, SurveyDBM, ScheduledSurveyDBM, SurveyQuestionDBM, QuestionDBM, SurveyResponseDBM
from tg_bot.handlers.common.message_service import MessageService
from tg_bot.handlers.doctor.survey_models import Question, ScheduledSurvey
from tg_bot.utils.time_validator import TimeValidator
from tg_bot.utils.data_validator import DateValidator

class ScheduleSurveyService:
    @staticmethod
    async def _get_or_create_survey(
        state: FSMContext,
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
    async def get_survey(
        state: FSMContext
    ):
        survey = await ScheduleSurveyService._get_or_create_survey(state)

        return survey.get_survey()

    @staticmethod
    async def clear_schedule_data(
        state: FSMContext,
    ):
        for STATE_KEY in ScheduledSurvey._STATE_KEYS:
            await MessageService.set_state_data(
                state=state,
                key=STATE_KEY,
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
    async def save_selected_survey(
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
            survey = await ScheduleSurveyService._get_or_create_survey(state)
            
            survey.save_selected_survey(survey_dbm)
            
            await ScheduleSurveyService._save_survey_changes(state, survey)
    
    @staticmethod
    async def get_selected_survey(
        state: FSMContext,
    ) -> Optional[SurveyDBM]:
        survey = await ScheduleSurveyService._get_or_create_survey(state)

        return survey.get_selected_survey()
    
    @staticmethod
    async def get_connected_patients(
        user_id: int,
    ) -> list[UserDBM]:
        async with get_cached_sqlalchemy_db().new_async_session() as session:
            patient_dbms = (await session.execute(
                sqlalchemy
                .select(UserDBM)
                .where(UserDBM.role == UserDBM.Roles.patient)
                # .join(DoctorPatientDBM, sqlalchemy.and_(
                #     DoctorPatientDBM.doctor_id == user_id,
                #     DoctorPatientDBM.patient_id == UserDBM.tg_id
                #     )
                # )
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


    @staticmethod
    async def save_selected_patient(
        state: FSMContext,
        patient_id: int
    ) -> None:
        async with get_cached_sqlalchemy_db().new_async_session() as session:
            user_dbm = (await session.execute(
                sqlalchemy
                .select(UserDBM)
                .where(UserDBM.tg_id == patient_id)
            )).scalar_one_or_none()

        survey = await ScheduleSurveyService._get_or_create_survey(state)

        survey.save_selected_patient(user_dbm=user_dbm)

        await ScheduleSurveyService._save_survey_changes(state, survey)

    @staticmethod
    async def get_selected_patient(
        state: FSMContext,
    ) -> Optional[UserDBM]:
        survey = await ScheduleSurveyService._get_or_create_survey(state)

        return survey.get_selected_patient()
    
    @staticmethod
    async def save_selected_doctor(
        state: FSMContext,
        user_id: int
    ):
        survey = await ScheduleSurveyService._get_or_create_survey(state)

        async with get_cached_sqlalchemy_db().new_async_session() as session:
            user_dbm = (await session.execute(
                sqlalchemy
                .select(UserDBM)
                .where(UserDBM.tg_id == user_id)
                .where(UserDBM.role == UserDBM.Roles.doctor)
            )).scalar_one()

        survey.save_selected_doctor(user_dbm=user_dbm)

        await ScheduleSurveyService._save_survey_changes(state, survey)

    @staticmethod
    async def schedule_suvey(
        state: FSMContext,
        user_id: int,
    ):
        await ScheduleSurveyService.save_selected_doctor(
            state=state, 
            user_id=user_id
        )

        survey_form = await ScheduleSurveyService._get_or_create_survey(state)
        
        survey = survey_form.get_survey()

        async with get_cached_sqlalchemy_db().new_async_session() as session:
            schedule_survey = ScheduledSurveyDBM(
                survey_id=survey.survey_dbm.id,
                patient_id=survey.patient_dbm.tg_id,
                doctor_id=survey.doctor_dbm.tg_id,
                frequency_type=survey.frequency_type,
                times_per_day=survey.times_per_day,
                interval_days=survey.interval_days,
                start_date=survey.start_date,
                end_date=survey.end_date,
                scheduled_times=survey.schedule_times,
                reminder_interval_hours=survey.reminder_interval_hours,
                next_scheduled_date=survey.start_date,
            )

            session.add(schedule_survey)
            await session.commit()

        await ScheduleSurveyService.clear_schedule_data(
            state=state,
        )

    
    @staticmethod
    async def get_all_surveys(
        user_tg_id: int
    ) -> list[SurveyDBM]:
        async with get_cached_sqlalchemy_db().new_async_session() as async_session:
            surveys_dbms = (await async_session.execute(
                sqlalchemy
                .select(SurveyDBM)
                .where(SurveyDBM.created_by == user_tg_id)
                .where(SurveyDBM.is_active)
            )).scalars().unique().all()
            
            return surveys_dbms


    @staticmethod
    async def get_questions_by_survey(
        survey_id: int
    ) -> list[QuestionDBM]:
        async with get_cached_sqlalchemy_db().new_async_session() as async_session:
            survey_question_dbms = (await async_session.execute(
                sqlalchemy
                .select(SurveyQuestionDBM)
                .where(SurveyQuestionDBM.survey_id == survey_id)
                .options(
                    joinedload(SurveyQuestionDBM.question)
                )
            )).scalars().unique().all()
            
            return [survey_question_dbm.question for survey_question_dbm in survey_question_dbms]
        

    @staticmethod
    async def _get_statistic_by_params(
        survey_id: int,
        scheduled_date: date,
        scdeduled_time: time,
        user_id: int,
        async_session: AsyncSession
    ) -> list[str]:
        responses = (await async_session.execute(
            sqlalchemy
            .select(SurveyResponseDBM)
            .options(
                joinedload(SurveyResponseDBM.scheduled_survey)
            )
            .where(sqlalchemy.func.date(SurveyResponseDBM.creation_dt) == scheduled_date)
            .where(ScheduledSurveyDBM.survey_id == survey_id)
            .where(SurveyResponseDBM.scheduled_time == scdeduled_time)
            .where(SurveyResponseDBM.patient_id == user_id)
        )).scalars().unique().all()
        

        response_answers = [
            response.answer for response in responses
            if response.scheduled_survey.survey_id == survey_id
        ]

        return response_answers
    
    @staticmethod
    async def get_survey_responses_for_all_time(
        survey_id: int
    ):
        async with get_cached_sqlalchemy_db().new_async_session() as async_session:
            # Получаем все уникальные даты, когда были ответы для данного survey_id
            dates_result = await async_session.execute(
                sqlalchemy.select(
                    sqlalchemy.func.date(SurveyResponseDBM.creation_dt).label('response_date')
                )
                .join(ScheduledSurveyDBM, SurveyResponseDBM.scheduled_survey_id == ScheduledSurveyDBM.id)
                .where(ScheduledSurveyDBM.survey_id == survey_id)
                .where(SurveyResponseDBM.creation_dt.is_not(None))
                .distinct()
            )
            
            dates = [row.response_date for row in dates_result]
            
            responses_for_all_time = []

            for curr_date in dates:
                # Получаем все ответы для текущей даты и survey_id
                responses_result = await async_session.execute(
                    sqlalchemy.select(SurveyResponseDBM)
                    .join(ScheduledSurveyDBM, SurveyResponseDBM.scheduled_survey_id == ScheduledSurveyDBM.id)
                    .options(
                        joinedload(SurveyResponseDBM.scheduled_survey),
                        joinedload(SurveyResponseDBM.patient)  # Добавляем загрузку пользователя
                    )
                    .where(sqlalchemy.func.date(SurveyResponseDBM.creation_dt) == curr_date)
                    .where(ScheduledSurveyDBM.survey_id == survey_id)
                )

                responses = responses_result.scalars().unique().all()
                
                # Получаем уникальные запланированные времена для текущего дня
                scheduled_times = list({
                    response.scheduled_time for response in responses 
                    if response.scheduled_time is not None
                })
                
                # Словарь для хранения данных по текущей дате
                date_data = {}
                
                for scheduled_time in scheduled_times:
                    # Получаем уникальных пользователей для данного времени
                    users = list({
                        response.patient_id for response in responses
                        if response.scheduled_time == scheduled_time
                    })
                    
                    time_data = {}
                    
                    for user_id in users:
                        user_reponces = await ScheduleSurveyService._get_statistic_by_params(
                            survey_id=survey_id,
                            scheduled_date=curr_date,
                            scdeduled_time=scheduled_time,
                            user_id=user_id,
                            async_session=async_session,
                        )

                        adjusted_time = (datetime.combine(curr_date, scheduled_time) + timedelta(hours=5)).time()

                        responses_for_all_time.append((user_id, curr_date, adjusted_time, user_reponces))
                    date_data[scheduled_time] = time_data
                
            return responses_for_all_time