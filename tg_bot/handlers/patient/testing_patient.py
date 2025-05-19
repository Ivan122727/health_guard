from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from shared.sqlalchemy_db_.sqlalchemy_model import UserDBM
from tg_bot.keyboards import PatientAction
from tg_bot.handlers.common.message_service import MessageService
from tg_bot.handlers.patient.patient_service import PatientService
from tg_bot.keyboards import PatientKeyboard
from tg_bot.blanks import PatientBlank
from tg_bot.states.patient import ConnectToDoctorStates

router = Router()


async def proccess_current_question(
    message: Message,
    state: FSMContext,
    keyboard: type[PatientKeyboard],
    blank: type[PatientBlank],
    user_dbm: type[UserDBM],
    from_cq: bool = True,
):
    patient_survey = await PatientService.get_survey(
        state=state,
        message_id=message.message_id,
    )

    curr_question = patient_survey.get_current_question()

    await message.bot.edit_message_text(
        text=blank.get_survey_question_blank(
            survey_title=patient_survey.title,
            question_text=curr_question.question.question_text,
            question_number=curr_question.order_index,
            total_questions=patient_survey.count_question,
        ),
        chat_id=user_dbm.tg_id,
        message_id=message.message_id,
    )
    await message.bot.edit_message_reply_markup(
        chat_id=user_dbm.tg_id,
        message_id=message.message_id,
        reply_markup=keyboard.get_survey_question_keyboard(
            question_id=curr_question.id,
            options=curr_question.question.answer_options,
            has_previous=bool(patient_survey.curr_question_index > 0)
        )
    )

    if not from_cq:
        await MessageService.remove_previous_message(
            bot=message.bot,
            user_id=user_dbm.tg_id,
            message_id=message.message_id,
        )


@router.callback_query(F.data.startswith(PatientAction.START_SURVEY))
async def handle_current_question(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[PatientKeyboard],
    blank: type[PatientBlank],
    user_dbm: type[UserDBM]
):
    notification_id = await MessageService.get_value_from_callback_data(callback_query.data)

    survey_can_be_passed = await PatientService.survey_can_be_passed(
        state=state,
        notification_id=notification_id,
        message_id=callback_query.message.message_id
    )
    
    if survey_can_be_passed == False:
        callback_query.answer("Вы уже проходили или не успели вовремя!")
        
        await callback_query.message.delete()

    await proccess_current_question(
        message=callback_query.message,
        state=state,
        keyboard=keyboard,
        blank=blank,
        user_dbm=user_dbm,
    )



@router.callback_query(F.data.startswith(PatientAction.ANSWER_QUESTION))
async def handle_answer_question(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[PatientKeyboard],
    blank: type[PatientBlank],
    user_dbm: type[UserDBM]
):
    answer_option = await MessageService.get_value_from_callback_data(
        callback_data=callback_query.data,
        position_index=3,
        type=str,
    )

    print(f"{answer_option=}")
    
    patient_survey = await PatientService.get_survey(
        state=state,
        message_id=callback_query.message.message_id,
    )

    patient_survey.set_answer(answer_option)

    PatientService.save_modificate(
        state=state, 
        message_id=callback_query.message.message_id,
        modificated_survey=patient_survey
    )


    if len(patient_survey.answers) == patient_survey.count_question:
        await callback_query.message.delete()
        
        await callback_query.answer("Тест был пройден!")
        await PatientService.save_test_attemp(
            state=state,
            survey=patient_survey,
            message_id=callback_query.message.message_id,
        )

    else:
        await proccess_current_question(
            message=callback_query.message,
            state=state,
            keyboard=keyboard,
            blank=blank,
            user_dbm=user_dbm,
        )

@router.callback_query(F.data.startswith(PatientAction.PREV_QUESTION))
async def set_prev_question(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[PatientKeyboard],
    blank: type[PatientBlank],
    user_dbm: type[UserDBM]
):
    patient_survey = await PatientService.get_survey(
        state=state,
        message_id=callback_query.message.message_id,
    )

    patient_survey.set_prev_question()

    PatientService.save_modificate(
        state=state, 
        message_id=callback_query.message.message_id,
        modificated_survey=patient_survey
    )

    await proccess_current_question(
        message=callback_query.message,
        state=state,
        keyboard=keyboard,
        blank=blank,
        user_dbm=user_dbm,
    )