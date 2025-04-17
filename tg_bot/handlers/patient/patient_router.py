from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from shared.sqlalchemy_db_.sqlalchemy_model import UserDBM
from tg_bot.keyboards import PatientAction
from tg_bot.handlers.common.message_service import MessageService
from tg_bot.handlers.patient.patient_service import PatientService
from tg_bot.keyboards import PatientKeyboard
from tg_bot.blanks import PatientBlank

router = Router()

@router.callback_query(F.data.startswith(PatientAction.CONNECT_TO_DOCTOR))
async def handle_select_doctor_request(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[PatientKeyboard],
    blank: type[PatientBlank],
):
    await callback_query.answer()

    page = await PatientService.get_number_from_callback_data(callback_query.data)

    available_doctors = await PatientService.get_available_doctors()

    await MessageService.edith_managed_message(
        bot=callback_query.bot,
        user_id=callback_query.from_user.id,
        text=blank.get_doctor_selection_blank(),
        reply_markup=keyboard.get_doctor_selection_keyboard(doctors=available_doctors, page=page),
        state=state,
        previous_message_key="start_msg_id",
        message_id_storage_key="start_msg_id",
        message=callback_query.message,
    )

@router.callback_query(F.data.startswith(PatientAction.SELECT_DOCTOR))
async def handle_confirm_selected_doctor(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[PatientKeyboard],
    blank: type[PatientBlank],
):
    selected_doctor_id = await PatientService.get_number_from_callback_data(callback_query.data)
    
    doctor_dbm = await PatientService.get_selected_doctor(selected_doctor_id)

    await MessageService.edith_managed_message(
        bot=callback_query.bot,
        user_id=callback_query.from_user.id,
        text=blank.get_selected_doctor_confirm_blank(doctor_dbm),
        reply_markup=keyboard.get_selected_doctor_keyboard(doctor_dbm.tg_id),
        state=state,
        previous_message_key="start_msg_id",
        message_id_storage_key="start_msg_id"
    )

@router.callback_query(F.data.startswith(PatientAction.CONFIRM_SELECTED_DOCTOR))
async def handle_select_doctor(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[PatientKeyboard],
    blank: type[PatientBlank],
    user_dbm: type[UserDBM]
):
    selected_doctor_id = await PatientService.get_number_from_callback_data(callback_query.data)

    if await PatientService.is_patient_has_connected(callback_query.from_user.id):
        await callback_query.answer(f"Вы уже закреплены к доктору!")
    else:
        await PatientService.connect_patient_to_doctor(
            user_id=callback_query.from_user.id,
            doctor_id=selected_doctor_id
        )
        await callback_query.answer(f"Связь с {selected_doctor_id} создана!")

    await MessageService.edith_managed_message(
        bot=callback_query.bot,
        user_id=callback_query.from_user.id,
        text=blank.get_default_blank(user_dbm.full_name),
        reply_markup=keyboard.get_default_keyboard(),
        state=state,
        previous_message_key="start_msg_id",
        message_id_storage_key="start_msg_id"
    )

@router.callback_query(F.data.startswith(PatientAction.CANCEL_CONNECT_TO_DOCTOR))
async def handle_cancel_connect_to_doctor(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[PatientKeyboard],
    blank: type[PatientBlank],
    user_dbm: type[UserDBM]
) -> None:
    """
    Обработка начального сообщения от пользователя
    
    Args:
        message: Входящее сообщение Telegram
        keyboard: Фабрика клавиатур
        blank: Фабрика шаблонов сообщений
    """
    await MessageService.edith_managed_message(
        bot=callback_query.bot,
        user_id=callback_query.from_user.id,
        text=blank.get_default_blank(user_dbm.full_name),
        reply_markup=keyboard.get_default_keyboard(),
        state=state,
        previous_message_key="start_msg_id",
        message_id_storage_key="start_msg_id",
        message=callback_query.message,
    )

    await callback_query.answer("Закрепление к доктору было отменено!")