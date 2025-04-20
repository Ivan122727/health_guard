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
    _STATE_KEY_SURVEY_NOT_CONFIRMED_TITLE = "survey_not_confirmed_title"

    @staticmethod
    async def get_selected_doctor(
        doctor_id: int
    ) -> UserDBM:
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
    async def get_value_from_callback_data(
        callback_data: str, 
        position_index: int = 2, 
        default_value: int = 0,
        sep: str = ":",
        type: type = int
    ) -> int:
        try:
            value = type(callback_data.split(sep=sep)[position_index - 1])
        except (IndexError, ValueError):
            value = default_value
        
        return value

    @staticmethod
    async def _get_or_create_survey(
        state: FSMContext
    ) -> Survey:
        survey: Survey = await MessageService.get_state_data(
            state=state, key=DoctorService._STATE_KEY_SURVEY,
        )

        if survey is None:
            survey = Survey()
        
        return survey

    @staticmethod
    async def save_not_confirmed_title(
        state: FSMContext,
        title: str
    ):
        await MessageService.set_state_data(
            state=state,
            key=DoctorService._STATE_KEY_SURVEY_NOT_CONFIRMED_TITLE,
            value=title
        )

    @staticmethod
    async def confirm_survey_title(
        state: FSMContext,
    ) -> None:
        title = await MessageService.get_state_data(
            state=state,
            key=DoctorService._STATE_KEY_SURVEY_NOT_CONFIRMED_TITLE,
        )
        if title:
            survey = await DoctorService._get_or_create_survey(state)

            survey.edith_survey_title(title=title)

            await DoctorService._save_survey_changes(
                state=state,
                survey=survey,
            )

            await MessageService.set_state_data(
                state=state,
                key=DoctorService._STATE_KEY_SURVEY_NOT_CONFIRMED_TITLE,
                value=None
            )
    
    @staticmethod
    async def get_confirmed_survey_title(
        state: FSMContext,
    ):
        survey = await DoctorService._get_or_create_survey(state)

        return survey.title

    @staticmethod
    async def _save_survey_changes(
        state: FSMContext,
        survey: Survey
    ) -> None:
        await MessageService.set_state_data(
            state=state,
            key=DoctorService._STATE_KEY_SURVEY,
            value=survey,
        )

    @staticmethod
    async def _get_question_id_to_edit(
        state: FSMContext
    ) -> str:
        return await MessageService.get_state_data(
            state=state, 
            key=DoctorService._STATE_KEY_EDIT_QUESTION_ID,
        )
    
    @staticmethod
    async def _has_question_to_edit(
        state: FSMContext
    ) -> bool:
        survey = await DoctorService._get_or_create_survey(state)

        question_id = await DoctorService._get_question_id_to_edit(state)

        return question_id and survey.get_question_by_id(question_id)

    @staticmethod
    async def save_edit_question_id(
        state: FSMContext,
        question_id: str
    ):
        survey = await DoctorService._get_or_create_survey(state)

        await MessageService.set_state_data(
            state=state,
            key=DoctorService._STATE_KEY_EDIT_QUESTION_ID,
            value=question_id,
        )        

    @staticmethod
    async def add_question_to_survey(
        state: FSMContext,
        text: Optional[str] = None,
        options: Optional[str] = None,
        is_from_template: bool = False,
        template_question_id: Optional[int] = None,
    ) -> None:
        survey = await DoctorService._get_or_create_survey(state)

        survey.add_question(
            text=text,
            options=options,
            is_from_template=is_from_template,
            template_question_id=template_question_id,
        )

        await DoctorService._save_survey_changes(
            state=state,
            survey=survey,
        )

    @staticmethod
    async def edit_question_in_survey(
        state: FSMContext,
        text: Optional[str] = None,
        options: Optional[str] = None,
        is_from_template: bool = False,
        template_question_id: Optional[int] = None,
    ) -> None:
        if await DoctorService._has_question_to_edit(state):
            survey = await DoctorService._get_or_create_survey(state)
            
            edit_question_id = await DoctorService._get_question_id_to_edit(state)

            survey.edit_question(
                question_id=edit_question_id,
                new_text=text,
                new_options=options,
                is_from_template=is_from_template,
                template_question_id=template_question_id,
            )

            survey.set_current_question(edit_question_id)

            await MessageService.set_state_data(
                state=state,
                key=DoctorService._STATE_KEY_EDIT_QUESTION_ID,
                value=None,
            )
        
            await DoctorService._save_survey_changes(
                state=state,
                survey=survey,
            )

    @staticmethod
    async def add_or_edit_question_text_in_survey(
        state: FSMContext,
        text: str,
        is_from_template: bool = False,
        template_question_id: Optional[int] = None
    ) -> None:
        if await DoctorService._has_question_to_edit(state):
            await DoctorService.edit_question_in_survey(
                state=state,
                text=text,
                is_from_template=is_from_template,
                template_question_id=template_question_id,
            )
        else:
            await DoctorService.add_question_to_survey(
                state=state,
                text=text,
                is_from_template=is_from_template,
                template_question_id=template_question_id,
            )    

    @staticmethod
    async def is_valid_answer_options(
        raw_options: str
    ) -> bool:
        return 1 < len(raw_options.split("\n")) < 11 

    @staticmethod
    async def parse_answer_options(
        raw_options: str
    ) -> list[str]:
        return list(raw_options.split("\n"))

    @staticmethod
    async def add_options_to_current_question(
        state: FSMContext,
        answer_options: list[str]
    ) -> None:
        survey = await DoctorService._get_or_create_survey(state) 

        curr_question = survey.get_current_question()
        
        if curr_question and curr_question.is_from_template is False:
            survey.edit_question(
                question_id=curr_question.id,
                new_text=curr_question.text,
                new_options=answer_options
            )

            await DoctorService._save_survey_changes(
                state=state,
                survey=survey,
            )

    @staticmethod
    async def get_survey_questions(
        state: FSMContext,
    ) -> list[Question]:
        survey = await DoctorService._get_or_create_survey(state)

        return survey.get_active_questions()

    @staticmethod
    async def get_count_questions_in_survey(
        state: FSMContext
    ) -> int:
        survey = await DoctorService._get_or_create_survey(state)
        
        return survey.count_valid_questions
    
    @staticmethod
    async def get_current_question(
        state: FSMContext,
    ) -> Question:
        survey = await DoctorService._get_or_create_survey(state)
        return survey.get_current_question()

    @staticmethod
    async def remove_current_question(
        state: FSMContext,
    ) -> None:
        survey = await DoctorService._get_or_create_survey(state)
        
        current_question = survey.get_current_question()
        
        if current_question:
            survey.remove_question(current_question.id)
            await DoctorService._save_survey_changes(state, survey)

    @staticmethod
    async def get_question_by_id(
        state: FSMContext,
        question_id: str
    ) -> Optional[Question]:
        survey = await DoctorService._get_or_create_survey(state)
        return survey.get_question_by_id(question_id)

    @staticmethod
    async def set_current_question(
        state: FSMContext,
        question_id: str
    ):
        survey = await DoctorService._get_or_create_survey(state)
        return survey.set_current_question(question_id)

    @staticmethod
    async def get_current_question_number(
        state: FSMContext
    ) -> int:
        survey = await DoctorService._get_or_create_survey(state)
        
        questions = survey.get_active_questions()
        try:
            question_number = questions.index(survey.get_current_question())
        except ValueError:
            question_number = -1

        return question_number + 1


    @staticmethod
    async def _get_question_by_offset(
        state: FSMContext,
        step: int,

    ) -> Optional[Question]:
        survey = await DoctorService._get_or_create_survey(state)
        
        current_question = survey.get_current_question()
        
        if not current_question:
            return None

        try:
            questions = survey.get_active_questions()

            current_question_index = questions.index(current_question)

            if current_question_index + step < 0:
                return None

            return questions[current_question_index + step]
        except IndexError:
            return None

    @staticmethod
    async def get_previous_question(
        state: FSMContext,
    ) -> Optional[Question]:
        return await DoctorService._get_question_by_offset(
            state=state, 
            step=-1
        )

    @staticmethod
    async def get_next_question(
        state: FSMContext,
    ) -> Optional[Question]:
        return await DoctorService._get_question_by_offset(
            state=state, 
            step=1
        )
    
    @staticmethod
    async def _get_template_question_from_db(
        user_id: int,
        template_question_id: int
    ) -> Optional[QuestionDBM]:
        async with get_cached_sqlalchemy_db().new_async_session() as session:
            question_dbm = (await session.execute(
                sqlalchemy
                .select(QuestionDBM)
                .where(QuestionDBM.id == template_question_id)
                .where(
                    (QuestionDBM.created_by == user_id) |
                    (QuestionDBM.is_public)
                )
            )).scalar()
            
        return question_dbm
    
    @staticmethod
    async def add_template_question_to_survey(
        state: FSMContext,
        user_id: int,
        template_question_id: int,
    ) -> bool:
        question_dbm = await DoctorService._get_template_question_from_db(
            user_id=user_id, 
            template_question_id=template_question_id,
        )

        if question_dbm is None:
            return False

        survey = await DoctorService._get_or_create_survey(state)

        survey.add_question(
            text=question_dbm.question_text,
            options=question_dbm.answer_options,
            is_from_template=True,
            template_question_id=question_dbm.id
        )

        await DoctorService._save_survey_changes(
            state=state,
            survey=survey,
        )

        return True
    
    @staticmethod
    async def add_or_edit_template_question_to_survey(
        state: FSMContext,
        user_id: int,
        template_question_id: int
    ) -> bool:
        question_dbm = await DoctorService._get_template_question_from_db(
            user_id=user_id,
            template_question_id=template_question_id,
        )
        if question_dbm is None:
            return False

        survey = await DoctorService._get_or_create_survey(state)

        if await DoctorService._has_question_to_edit(state):
            question_id = await DoctorService._get_question_id_to_edit(
                state=state
            )

            survey.edit_question(
                question_id=question_id,
                new_text=question_dbm.question_text,
                new_options=question_dbm.answer_options,
                is_from_template=True,
                template_question_id=template_question_id,
            )

            await MessageService.set_state_data(
                state=state,
                key=DoctorService._STATE_KEY_EDIT_QUESTION_ID,
                value=None,
            )
        else:
            survey.add_question(
                text=question_dbm.question_text,
                options=question_dbm.answer_options,
                is_from_template=True,
                template_question_id=question_dbm.id
            )

        await DoctorService._save_survey_changes(
            state=state,
            survey=survey
        )

        return True

    @staticmethod
    async def _create_survey_record(
        session: AsyncSession, 
        title: str, 
        user_id: int
    ) -> SurveyDBM:
        survey = SurveyDBM(
            title=title, 
            created_by=user_id
        )
        session.add(survey)
        await session.flush()
        await session.refresh(survey)
        return survey

    @staticmethod
    async def _create_question_record(
        session: AsyncSession, 
        user_id: int,
        survey_id: int,
        question: Question,
        order: int,
    ) -> bool:
        if question.is_from_template and question.template_question_id:
            try:
                question_dbm = (await session.execute(
                    sqlalchemy
                    .select(QuestionDBM)
                    .where(QuestionDBM.id == question.template_question_id)
                    .where(
                        (QuestionDBM.created_by == user_id) |
                        (QuestionDBM.is_public)
                    )
                )).scalar_one()
            except Exception as e:
                print("wwewe\n\n")
                print(str(e))
                return False
        else:
            if question.text is None or question.options is None:
                print("Nooooooo\n\n")
                return False

            question_dbm = QuestionDBM(
                created_by=user_id,
                question_type=QuestionDBM.QuestionType.CHOICE,
                question_text=question.text,
                answer_options=question.options,
            )

            session.add(question_dbm)
            await session.flush()
            await session.refresh(question_dbm)

        survey_question_dbm = SurveyQuestionDBM(
            survey_id=survey_id,
            question_id=question_dbm.id,
            order_index=order
        )
        session.add(survey_question_dbm)
        await session.flush()
        await session.refresh(survey_question_dbm)
        
        return True

    @staticmethod
    async def clear_survey_data(
        state: FSMContext,
        user_id: int
    ):
        await MessageService.set_state_data(
            state,
            key=DoctorService._STATE_KEY_SURVEY,
            value=None
        )

    @staticmethod
    async def save_survey_in_db(
        state: FSMContext,
        user_id: int
    ) -> bool:
        survey = await DoctorService._get_or_create_survey(state)

        if survey.count_valid_questions == 0:
            return False
        
        async with get_cached_sqlalchemy_db().new_async_session() as session:
            survey_dbm = await DoctorService._create_survey_record(
                session=session,
                title=survey.title,
                user_id=user_id
            )

            for order, question in enumerate(survey.get_active_questions(), 1):
                added = await DoctorService._create_question_record(
                    session=session,
                    user_id=user_id,
                    survey_id=survey_dbm.id,
                    question=question,
                    order=order
                )
            
            await session.commit()
        
        await DoctorService.clear_survey_data(
            state=state,
            user_id=user_id,
        )

        return True
    
    @staticmethod
    async def get_available_questions(
        user_id: int
    ) -> list[QuestionDBM]:
        async with get_cached_sqlalchemy_db().new_async_session() as session:
            question_dbms = (await session.execute(
                sqlalchemy
                .select(QuestionDBM)
                .where(
                    (QuestionDBM.created_by == user_id) |
                    (QuestionDBM.is_public)
                )
            )).scalars().unique().all()
        
        return question_dbms