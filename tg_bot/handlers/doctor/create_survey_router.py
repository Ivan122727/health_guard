from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from shared.sqlalchemy_db_.sqlalchemy_model.user import UserDBM
from tg_bot.handlers.common.message_service import MessageService
from tg_bot.handlers.doctor.doctor_service import DoctorService
from tg_bot.handlers.doctor.survey_class import Survey
from tg_bot.keyboards import DoctorAction, DoctorKeyboard
from tg_bot.blanks import DoctorBlank
from tg_bot.states.survey import CreateNewSurveyStates

router = Router()

@router.callback_query(F.data.startswith(DoctorAction.CREATE_SURVEY.value))
async def handle_survey_type_select(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    await MessageService.edith_managed_message(
        bot=callback_query.bot,
        user_id=callback_query.from_user.id,
        text=blank.get_choose_type_survey_blank(),
        reply_markup=keyboard.get_survey_type_selection_keyboard(),
        state=state,
        previous_message_key="start_msg_id",
        message_id_storage_key="start_msg_id",
        message=callback_query.message,
    )

@router.callback_query(F.data.startswith(DoctorAction.CREATE_NEW_SURVEY.value))
async def handle_confirm_new_survey_type(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    await MessageService.edith_managed_message(
        bot=callback_query.bot,
        user_id=callback_query.from_user.id,
        text=blank.get_create_from_scratch_blank(),
        reply_markup=keyboard.get_confirm_create_new_survey_keyboard(),
        state=state,
        previous_message_key="start_msg_id",
        message_id_storage_key="start_msg_id",
        message=callback_query.message,
    )

@router.callback_query(F.data.startswith(DoctorAction.CREATE_TEMPLATE_SURVEY.value))
async def handle_confirm_template_survey_type(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    await MessageService.edith_managed_message(
        bot=callback_query.bot,
        user_id=callback_query.from_user.id,
        text=blank.get_use_template_blank(),
        reply_markup=keyboard.get_confirm_create_template_survey_keyboard(),
        state=state,
        previous_message_key="start_msg_id",
        message_id_storage_key="start_msg_id",
        message=callback_query.message,
    )


@router.callback_query(F.data.startswith(DoctorAction.CONFIRM_CREATE_NEW_SURVEY.value))
async def handle_confirm_new_survey_type(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    await MessageService.edith_managed_message(
        bot=callback_query.bot,
        user_id=callback_query.from_user.id,
        text=blank.get_create_from_scratch_blank(step="enter_question"),
        reply_markup=keyboard.get_survey_management_keyboard(),
        state=state,
        previous_message_key="start_msg_id",
        message_id_storage_key="start_msg_id",
        message=callback_query.message,
        new_state=CreateNewSurveyStates.waiting_new_question_text,
    )

@router.callback_query(F.data.startswith(DoctorAction.CONFIRM_CREATE_TEMPLATE_SURVEY.value))
async def handle_confirm_template_survey_type(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    await MessageService.edith_managed_message(
        bot=callback_query.bot,
        user_id=callback_query.from_user.id,
        text=blank.get_use_template_blank(),
        reply_markup=keyboard.get_confirm_create_new_survey_keyboard(),
        state=state,
        previous_message_key="start_msg_id",
        message_id_storage_key="start_msg_id",
        message=callback_query.message,
    )


# Добавление текста вопроса в новый опрос
@router.message(CreateNewSurveyStates.waiting_new_question_text)
async def handle_add_new_question_text(
    message: Message,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    # Добавляем текст в опрос
    await DoctorService.add_or_edith_question_text_in_survey(
        state=state,
        question_text=message.text,
    )

    await MessageService.edith_managed_message(
        bot=message.bot,
        user_id=message.from_user.id,
        text=blank.get_create_from_scratch_blank(step="enter_options", current_question=message.text),
        reply_markup=keyboard.get_survey_management_keyboard(),
        state=state,
        previous_message_key="start_msg_id",
        message_id_storage_key="start_msg_id",
        new_state=CreateNewSurveyStates.waiting_new_question_options
    )
    
    # Удаление сообщения пользователя
    await MessageService.remove_previous_message(
        bot=message.bot, 
        user_id=message.from_user.id,
        message_id=message.message_id
    )

# Добавление вариантов ответа на вопрос в новый опрос
@router.message(CreateNewSurveyStates.waiting_new_question_options)
async def handle_add_new_question_options(
    message: Message,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    answer_options = await DoctorService.parse_question_answer_options(
        raw_question_answer_options=message.text
    )
    await DoctorService.add_add_answer_options_in_survey(
        state=state,
        answer_options=answer_options
    )
    
    count_questions = await DoctorService.get_count_questions(state=state)

    await MessageService.edith_managed_message(
        bot=message.bot,
        user_id=message.from_user.id,
        text=blank.get_create_from_scratch_blank(step="enter_question", count_questions=count_questions),
        reply_markup=keyboard.get_survey_management_keyboard(),
        state=state,
        previous_message_key="start_msg_id",
        message_id_storage_key="start_msg_id",
        new_state=CreateNewSurveyStates.waiting_new_question_text
    )
    
    # Удаление сообщения пользователя
    await MessageService.remove_previous_message(
        bot=message.bot, 
        user_id=message.from_user.id,
        message_id=message.message_id
    )

@router.callback_query(F.data.startswith(DoctorAction.EDITH_SURVEY.value))
async def handle_edith_survey(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    questions = await DoctorService.get_survey(state=state)
    for question in questions:
        print(f"{question.id=}, {question.text=}, {question.options=}, {question.is_active=}")
    
    await MessageService.edith_managed_message(
        bot=callback_query.bot,
        user_id=callback_query.from_user.id,
        text=blank.get_default_blank(user_dbm.full_name),
        reply_markup=keyboard.get_edit_survey_keyboard(),
        state=state,
        previous_message_key="start_message_id",
        message_id_storage_key="start_message_id",
        message=callback_query.message,
    )    
    