from typing import Optional
import sqlalchemy
from aiogram.fsm.context import FSMContext

from shared.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from shared.sqlalchemy_db_.sqlalchemy_model import UserDBM
from tg_bot.handlers.common.message_service import MessageService
from tg_bot.handlers.doctor.survey_class import Survey

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

    @staticmethod
    async def add_or_edith_question_text_in_survey(
        state: FSMContext,
        question_text: str,
    ):
        survey: Survey = await MessageService.get_state_data(
            state=state, key="survey",
        )

        if survey is None:
            survey = Survey()

        question_id = await MessageService.get_state_data(
            state=state, 
            key="edith_question_id"
        )

        if question_id and survey.get_question_by_id(question_id):
            survey.edit_question(
                question_id=question_id,
                new_text=question_text
            )
            
            survey.set_current_question(question_id)
            
            await MessageService.set_state_data(
                state=state,
                key="edith_question_id",
                value=None,
            )
        else:
            survey.add_question(text=question_text)

        await MessageService.set_state_data(
            state=state,
            key="survey",
            value=survey,
        )

    @staticmethod
    async def parse_question_answer_options(
        raw_question_answer_options: str
    ) -> list[str]:
        return list(raw_question_answer_options.split())

    @staticmethod
    async def add_add_answer_options_in_survey(
        state: FSMContext,
        answer_options: list[str]
    ):
        survey: Survey = await MessageService.get_state_data(
            state=state, key="survey",
        )
        curr_question = survey.get_current_question()

        survey.edit_question(
            question_id=curr_question.id,
            new_text=curr_question.text,
            new_options=answer_options
        )

        await MessageService.set_state_data(
            state=state,
            key="survey",
            value=survey,
        )

    @staticmethod
    async def get_survey(
        state: FSMContext,
    ):
        survey: Survey = await MessageService.get_state_data(
            state=state, key="survey",
        )
        if survey is None:
            survey = Survey()
        
        return survey.get_active_questions()

    @staticmethod
    async def get_count_questions(
        state: FSMContext
    ):
        survey: Survey = await MessageService.get_state_data(
            state=state, key="survey",
        )
        if survey is None:
            survey = Survey()
        
        return survey.count_active_questions