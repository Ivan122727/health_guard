from typing import Optional
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext

from shared.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from shared.sqlalchemy_db_.sqlalchemy_model import UserDBM, QuestionDBM, SurveyDBM, SurveyQuestionDBM
from tg_bot.handlers.common.message_service import MessageService
from tg_bot.handlers.doctor.survey_class import Question, Survey

class DoctorService:
    _STATE_KEY_SURVEY = "survey"
    _STATE_KEY_EDIT_QUESTION_ID = "edit_question_id"
    
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
    async def get_number_from_callback_data(callback_data: str, position_index: int = 2, default_value: int = 0) -> int:
        try:
            num = int(callback_data.split(":")[position_index - 1])
        except (IndexError, ValueError):
            num = default_value
        
        return num

    @staticmethod
    async def get_or_create_survey(
        state: FSMContext
    ) -> Survey:
        survey: Survey = await MessageService.get_state_data(
            state=state, key=DoctorService._STATE_KEY_SURVEY,
        )

        if survey is None:
            survey = Survey()
        
        return survey

    @staticmethod
    async def save_survey_changes(
        state: FSMContext,
        survey: Survey
    ) -> None:
        await MessageService.set_state_data(
            state=state,
            key=DoctorService._STATE_KEY_SURVEY,
            value=survey,
        )

    @staticmethod
    async def get_question_id_to_edit(
        state: FSMContext
    ) -> int:
        return await MessageService.get_state_data(
            state=state, 
            key=DoctorService._STATE_KEY_EDIT_QUESTION_ID,
        )

    @staticmethod
    async def has_question_to_edit(
        state: FSMContext
    ) -> bool:
        survey = await DoctorService.get_or_create_survey(state)

        edit_question_id = await DoctorService.get_question_id_to_edit(state)

        return edit_question_id and survey.get_question_by_id(edit_question_id)

    @staticmethod
    async def add_question_to_survey(
        state: FSMContext,
        text: Optional[str],
        options: Optional[str]
    ):
        survey = await DoctorService.get_or_create_survey(state)

        survey.add_question(
            text=text,
            question_options=options,
        )

        await DoctorService.save_survey_changes(
            state=state,
            survey=survey,
        )

    @staticmethod
    async def edit_question_in_survey(
        state: FSMContext,
        text: Optional[str],
        options: Optional[str]
    ):
        if await DoctorService.has_question_to_edit(state):
            survey = await DoctorService.get_or_create_survey(state)
            
            edit_question_id = await DoctorService.get_question_id_to_edit(state)

            survey.edit_question(
                question_id=edit_question_id,
                new_text=text,
                question_options=options,
            )

            survey.set_current_question(edit_question_id)

            await MessageService.set_state_data(
                state=state,
                key=DoctorService._STATE_KEY_EDIT_QUESTION_ID,
                value=None,
            )
        
            await DoctorService.save_survey_changes(
                state=state,
                survey=survey,
            )

    @staticmethod
    async def add_or_edit_question_text_in_survey(
        state: FSMContext,
        text: str,
    ) -> None:
        if await DoctorService.has_question_to_edit(state):
            await DoctorService.edit_question_in_survey(
                state=state,
                text=text,
            )
        else:
            await DoctorService.add_question_to_survey(
                state=state,
                text=text,
            )    

    @staticmethod
    async def parse_answer_options(
        raw_options: str
    ) -> list[str]:
        return list(raw_options.split())

    @staticmethod
    async def add_options_to_current_question(
        state: FSMContext,
        answer_options: list[str]
    ):
        survey = await DoctorService.get_or_create_survey(state) 

        curr_question = survey.get_current_question()

        survey.edit_question(
            question_id=curr_question.id,
            new_text=curr_question.text,
            new_options=answer_options
        )

        await DoctorService.save_survey_changes(
            state=state,
            survey=survey,
        )

    @staticmethod
    async def get_survey_questions(
        state: FSMContext,
    ) -> list[Question]:
        survey = await DoctorService.get_or_create_survey(state)

        return survey.get_active_questions()

    @staticmethod
    async def get_count_questions_in_survey(
        state: FSMContext
    ):
        survey = await DoctorService.get_or_create_survey(state)
        
        return survey.count_active_questions
    
    @staticmethod
    async def get_current_question(
        state: FSMContext,
    ) -> Question:
        survey = await DoctorService.get_or_create_survey(state)
        return survey.get_current_question()

    @staticmethod
    async def _get_question_by_offset(
        state: FSMContext,
        step: int,

    ) -> Optional[Question]:
        survey = await DoctorService.get_or_create_survey(state)
        try:
            current_question = survey.get_current_question()
            
            questions = survey.get_active_questions()
            
            current_question_index = questions.index(current_question)
            
            return questions[current_question_index + step]
        except IndexError:
            return None

    @staticmethod
    async def get_previous_question(
        state: FSMContext,
    ):
        return await DoctorService._get_question_by_offset(
            state=state, 
            step=-1
        )

    @staticmethod
    async def get_next_question(
        state: FSMContext,
    ):
        return await DoctorService._get_question_by_offset(
            state=state, 
            step=1
        )

    @staticmethod
    async def _create_survey_record(
        async_session, 
        title: str, 
        user_id: int
    ) -> SurveyDBM:
        survey = SurveyDBM(
            title=title, 
            created_by=user_id
        )
        async_session.add(survey)
        await async_session.flush()
        await async_session.refresh(survey)
        return survey

    @staticmethod
    async def _create_question_record(
        async_session: AsyncSession, 
        user_id: int,
        survey_id: int,
        question: Question,
        order: int,
        is_new: bool = True,
    ) -> SurveyQuestionDBM:
        if is_new or True:
            question_dbm = QuestionDBM(
                created_by=user_id,
                question_type=QuestionDBM.QuestionType.CHOICE,
                question_text=question.text,
                answer_options=question.options,
            )

            async_session.add(question_dbm)
            await async_session.flush()
            await async_session.refresh(question_dbm)
        else:
            pass
        
        survey_question_dbm = SurveyQuestionDBM(
            survey_id=survey_id,
            question_id=question_dbm.id,
            order_index=order
        )
        async_session.add(question_dbm)
        await async_session.flush()

    @staticmethod
    async def save_survey_in_db(
        state: FSMContext,
        user_id: int
    ):
        survey = await DoctorService.get_or_create_survey(state)

        if survey.count_active_questions == 0:
            return
        
        questions = survey.get_active_questions()
        
        async with get_cached_sqlalchemy_db().new_async_session() as async_session:
            survey_dbm = await DoctorService._create_survey_record(
                async_session=async_session,
                title=survey.title,
                user_id=user_id
            )

            question_order = 1
            for question in questions:
                if question.options and question.text:
                    question_dbm = QuestionDBM(
                        question_text=question.text,
                        question_type=QuestionDBM.QuestionType.CHOICE,
                        created_by=user_id,
                        answer_options=question.options
                    )
                    async_session.add(question_dbm)
                    await async_session.flush()
                    await async_session.refresh(question_dbm)

                    survey_question_dbm = SurveyQuestionDBM(
                        survey_id=survey_dbm.id,
                        question_id=question_dbm.id,
                        order_index=question_order
                    )
                    
                    async_session.add(survey_question_dbm)
                    await async_session.flush()
                    await async_session.refresh(survey_question_dbm)

                    question_order += 1
            await async_session.commit()