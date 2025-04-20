from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from shared.sqlalchemy_db_.sqlalchemy_model.user import UserDBM
from tg_bot.handlers.common.message_service import MessageService
from tg_bot.handlers.doctor.doctor_service import DoctorService
from tg_bot.handlers.doctor.survey_class import Survey
from tg_bot.keyboards import DoctorAction, DoctorKeyboard
from tg_bot.blanks import DoctorBlank
from tg_bot.states.survey import CreateSurveyStates

router = Router()

@router.callback_query(F.data.startswith(DoctorAction.CREATE_TITLE_SURVEY.value))
async def handle_create_title_survey(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    count_questions = await DoctorService.get_count_questions_in_survey(state)
    
    await MessageService.edith_managed_message(
        bot=callback_query.bot,
        user_id=callback_query.from_user.id,
        text=blank.get_survey_title_input_blank(),
        reply_markup=keyboard.get_question_management_keyboard(count_questions),
        state=state,
        previous_message_key="start_msg_id",
        message_id_storage_key="start_msg_id",
        message=callback_query.message,
        new_state=CreateSurveyStates.waiting_new_title_survey
    )

async def proccess_edit_survey_title(
    message: Message,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM],
    change_title: bool = True
):
    if change_title:
        title = message.text
    else:
        title = await DoctorService.get_confirmed_survey_title(state)

    await MessageService.edith_managed_message(
        bot=message.bot,
        user_id=user_dbm.tg_id,
        text=blank.get_survey_title_confirmation_blank(title),
        reply_markup=keyboard.get_survey_title_keyboard(),
        state=state,
        previous_message_key="start_msg_id",
        message_id_storage_key="start_msg_id",
        new_state=CreateSurveyStates.waiting_new_title_survey
    )

    await DoctorService.save_not_confirmed_title(
        state=state,
        title=title,
    )

    if change_title:
        await MessageService.remove_previous_message(
            message.bot,
            user_id=user_dbm.tg_id,
            message_id=message.message_id,
        )

@router.message(CreateSurveyStates.waiting_new_title_survey)
async def handle_input_title_survey(
    message: Message,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    await proccess_edit_survey_title(
        message=message,
        state=state,
        keyboard=keyboard,
        blank=blank,
        user_dbm=user_dbm,
        change_title=True
    )

@router.callback_query(F.data.startswith(DoctorAction.EDIT_SURVEY_TITLE.value))
async def handle_edit_survey_title(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    await proccess_edit_survey_title(
        message=callback_query.message,
        state=state,
        keyboard=keyboard,
        blank=blank,
        user_dbm=user_dbm,
        change_title=False,
    )

async def proccess_handle_choose_type_question(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    count_questions = await DoctorService.get_count_questions_in_survey(state)

    await MessageService.edith_managed_message(
        bot=callback_query.bot,
        user_id=callback_query.from_user.id,
        text=blank.get_choose_type_survey_blank(),
        reply_markup=keyboard.get_question_type_selection_keyboard(count_questions),
        state=state,
        previous_message_key="start_msg_id",
        message_id_storage_key="start_msg_id",
        message=callback_query.message,
    )

@router.callback_query(F.data.startswith(DoctorAction.CONFIRM_TITLE_SURVEY.value))
async def handle_confirm_title_survey(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    await DoctorService.confirm_survey_title(
        state=state
    )

    await proccess_handle_choose_type_question(
        callback_query=callback_query,
        state=state,
        keyboard=keyboard,
        blank=blank,
        user_dbm=user_dbm
    )

@router.callback_query(F.data.startswith(DoctorAction.CHOOSE_TYPE_QUESTION.value))
async def handle_choose_type_question(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    await proccess_handle_choose_type_question(
        callback_query=callback_query,
        state=state,
        keyboard=keyboard,
        blank=blank,
        user_dbm=user_dbm
    )

@router.callback_query(F.data.startswith(DoctorAction.CREATE_NEW_QUESTION.value))
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
        reply_markup=keyboard.get_confirm_create_new_question_keyboard(),
        state=state,
        previous_message_key="start_msg_id",
        message_id_storage_key="start_msg_id",
        message=callback_query.message,
    )

@router.callback_query(F.data.startswith(DoctorAction.CREATE_TEMPLATE_QUESTION.value))
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
        reply_markup=keyboard.get_confirm_create_template_question_keyboard(),
        state=state,
        previous_message_key="start_msg_id",
        message_id_storage_key="start_msg_id",
        message=callback_query.message,
    )


@router.callback_query(F.data.startswith(DoctorAction.CONFIRM_CREATE_NEW_QUESTION.value))
async def handle_confirm_new_survey_type(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    count_questions = await DoctorService.get_count_questions_in_survey(state)

    await MessageService.edith_managed_message(
        bot=callback_query.bot,
        user_id=callback_query.from_user.id,
        text=blank.get_create_from_scratch_blank(step=blank.STATE_QUESTION_TEXT),
        reply_markup=keyboard.get_question_management_keyboard(count_questions=count_questions),
        state=state,
        previous_message_key="start_msg_id",
        message_id_storage_key="start_msg_id",
        message=callback_query.message,
        new_state=CreateSurveyStates.waiting_new_question_text,
    )

@router.callback_query(F.data.startswith(DoctorAction.CONFIRM_CREATE_TEMPLATE_QUESTION.value))
async def handle_confirm_template_survey_type(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    count_questions = await DoctorService.get_count_questions_in_survey(state)
    
    await MessageService.edith_managed_message(
        bot=callback_query.bot,
        user_id=callback_query.from_user.id,
        text=blank.get_use_template_blank(),
        reply_markup=keyboard.get_question_management_keyboard(count_questions),
        state=state,
        previous_message_key="start_msg_id",
        message_id_storage_key="start_msg_id",
        message=callback_query.message,
        new_state=CreateSurveyStates.waiting_template_question_id
    )

# Добавление текста вопроса в новый опрос
@router.message(CreateSurveyStates.waiting_new_question_text)
async def handle_add_new_question_text(
    message: Message,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    # Добавляем текст в опрос
    await DoctorService.add_or_edit_question_text_in_survey(
        state=state,
        text=message.text,
    )

    count_questions = await DoctorService.get_count_questions_in_survey(state)

    await MessageService.edith_managed_message(
        bot=message.bot,
        user_id=message.from_user.id,
        text=blank.get_create_from_scratch_blank(step=blank.STATE_QUESTION_OPTIONS, current_question=message.text),
        reply_markup=keyboard.get_question_management_keyboard(count_questions),
        state=state,
        previous_message_key="start_msg_id",
        message_id_storage_key="start_msg_id",
        new_state=CreateSurveyStates.waiting_new_question_options
    )
    
    # Удаление сообщения пользователя
    await MessageService.remove_previous_message(
        bot=message.bot, 
        user_id=message.from_user.id,
        message_id=message.message_id
    )

# Добавление вариантов ответа на вопрос в новый опрос
@router.message(CreateSurveyStates.waiting_new_question_options)
async def handle_add_new_question_options(
    message: Message,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    answer_options = await DoctorService.parse_answer_options(
        raw_options=message.text
    )
    await DoctorService.add_options_to_current_question(
        state=state,
        answer_options=answer_options
    )
    
    count_questions = await DoctorService.get_count_questions_in_survey(state=state)

    await MessageService.edith_managed_message(
        bot=message.bot,
        user_id=message.from_user.id,
        text=blank.get_create_from_scratch_blank(step=blank.STATE_QUESTION_TEXT, count_questions=count_questions),
        reply_markup=keyboard.get_question_management_keyboard(count_questions),
        state=state,
        previous_message_key="start_msg_id",
        message_id_storage_key="start_msg_id",
        new_state=CreateSurveyStates.waiting_new_question_text
    )
    
    # Удаление сообщения пользователя
    await MessageService.remove_previous_message(
        bot=message.bot, 
        user_id=message.from_user.id,
        message_id=message.message_id
    )

@router.message(CreateSurveyStates.waiting_template_question_id)
async def handle_add_template_question(
    message: Message,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    template_question_id = int(message.text)
    
    is_success = await DoctorService.add_or_edit_template_question_to_survey(
        state=state,
        user_id=message.from_user.id,
        template_question_id=template_question_id
    )
    
    count_questions = await DoctorService.get_count_questions_in_survey(state)

    if is_success:
        await MessageService.edith_managed_message(
            bot=message.bot,
            user_id=message.from_user.id,
            text=blank.get_use_template_blank(),
            reply_markup=keyboard.get_question_management_keyboard(count_questions),
            state=state,
            previous_message_key="start_msg_id",
            message_id_storage_key="start_msg_id",
            new_state=CreateSurveyStates.waiting_template_question_id,
        )
    else:
        await MessageService.edith_managed_message(
            bot=message.bot,
            user_id=message.from_user.id,
            text=blank.get_use_template_blank() + "\nnigger",
            reply_markup=keyboard.get_question_management_keyboard(count_questions),
            state=state,
            previous_message_key="start_msg_id",
            message_id_storage_key="start_msg_id",
            new_state=CreateSurveyStates.waiting_template_question_id,
        )
    
    # Удаление сообщения пользователя
    await MessageService.remove_previous_message(
        bot=message.bot, 
        user_id=message.from_user.id,
        message_id=message.message_id
    )

@router.callback_query(F.data.startswith(DoctorAction.SAVE_SURVEY.value))
async def handle_save_survey(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    survey_was_added = await DoctorService.save_survey_in_db(
        state=state,
        user_id=callback_query.from_user.id,
    )

    await MessageService.edith_managed_message(
        bot=callback_query.bot,
        user_id=callback_query.from_user.id,
        text=blank.get_default_blank(user_dbm.full_name),
        reply_markup=keyboard.get_default_keyboard(),
        state=state,
        previous_message_key="start_message_id",
        message_id_storage_key="start_message_id",
        message=callback_query.message,
        new_state=None
    )    

    if survey_was_added:
        await callback_query.answer("Опрос был создан!")
    else:
        await callback_query.answer("Создание опроса было отменено!")

@router.callback_query(F.data.startswith(DoctorAction.CANCEL_CREATE_SURVEY.value))
async def handle_cancel_create_survey(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    await MessageService.edith_managed_message(
        bot=callback_query.bot,
        user_id=callback_query.from_user.id,
        text=blank.get_default_blank(user_dbm.full_name),
        reply_markup=keyboard.get_default_keyboard(),
        state=state,
        previous_message_key="start_message_id",
        message_id_storage_key="start_message_id",
        message=callback_query.message,
        new_state=None
    )    

    await DoctorService.clear_survey_data(
        state=state,
        user_id=callback_query.from_user.id,
    ) 

    await callback_query.answer("Создание опроса было отменено!")


async def proccess_handle_edit_survey(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
):
    question = await DoctorService.get_current_question(state)

    await MessageService.edith_managed_message(
        bot=callback_query.bot,
        user_id=callback_query.from_user.id,
        text=blank.get_question_info(
            current_question=await DoctorService.get_current_question(state),
            question_number=await DoctorService.get_current_question_number(state),
            total_questions=await DoctorService.get_count_questions_in_survey(state),
        ),
        reply_markup=keyboard.get_edit_survey_keyboard(
            current_question=await DoctorService.get_current_question(state),
            previout_question=await DoctorService.get_previous_question(state),
            next_question=await DoctorService.get_next_question(state)
        ),
        state=state,
        previous_message_key="start_message_id",
        message_id_storage_key="start_message_id",
        message=callback_query.message,
        new_state=None
    )

@router.callback_query(F.data.startswith(DoctorAction.EDIT_SURVEY.value))
async def handle_edit_survey(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    await proccess_handle_edit_survey(
        callback_query=callback_query,
        state=state,
        keyboard=keyboard,
        blank=blank
    )

@router.callback_query(F.data.startswith(DoctorAction.SET_CURRENT_QUESTION.value))
async def handle_set_current_question(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    question_id = await DoctorService.get_value_from_callback_data(
        callback_data=callback_query.data,
        default_value=None,
        type=str,
    )
    
    if await DoctorService.get_question_by_id(state, question_id):
        await DoctorService.set_current_question(
            state=state,
            question_id=question_id
        )
    
    await proccess_handle_edit_survey(
        callback_query=callback_query,
        state=state,
        keyboard=keyboard,
        blank=blank
    )

@router.callback_query(F.data.startswith(DoctorAction.REMOVE_CURRENT_QUESTION.value))
async def handle_remove_current_question(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    await DoctorService.remove_current_question(state)
    
    await proccess_handle_edit_survey(
        callback_query=callback_query,
        state=state,
        keyboard=keyboard,
        blank=blank
    )

async def process_handle_create_question(
        callback_query: CallbackQuery,
        state: FSMContext,
        keyboard: type[DoctorKeyboard],
        blank: type[DoctorBlank],
        user_dbm: type[UserDBM],
        save_edit_question: bool = False,
):
    current_question = await DoctorService.get_current_question(state)

    count_questions = await DoctorService.get_count_questions_in_survey(state)

    if save_edit_question:
        await DoctorService.save_edit_question_id(
            state=state,
            question_id=current_question.id
        )

    if current_question.is_from_template:
        text=blank.get_use_template_blank()
        new_state=CreateSurveyStates.waiting_template_question_id
    else:
        text=blank.get_create_from_scratch_blank(step=blank.STATE_QUESTION_TEXT)
        new_state=CreateSurveyStates.waiting_new_question_text

    await MessageService.edith_managed_message(
        bot=callback_query.bot,
        user_id=callback_query.from_user.id,
        text=text,
        reply_markup=keyboard.get_question_management_keyboard(count_questions=count_questions),
        state=state,
        previous_message_key="start_msg_id",
        message_id_storage_key="start_msg_id",
        message=callback_query.message,
        new_state=new_state,
    )

@router.callback_query(F.data.startswith(DoctorAction.FINISH_EDITING.value))
async def handle_finish_editing(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    await process_handle_create_question(
        callback_query=callback_query,
        state=state,
        keyboard=keyboard,
        blank=blank,
        user_dbm=user_dbm,
    )

@router.callback_query(F.data.startswith(DoctorAction.EDIT_QUESTION.value))
async def handle_edit_current_question(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    await process_handle_create_question(
        callback_query=callback_query,
        state=state,
        keyboard=keyboard,
        blank=blank,
        user_dbm=user_dbm,
        save_edit_question=True
    )