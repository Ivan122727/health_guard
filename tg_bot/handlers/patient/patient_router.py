from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from shared.sqlalchemy_db_.sqlalchemy_model import UserDBM
from tg_bot.keyboards import PatientAction
from tg_bot.handlers.common.message_service import MessageService
from tg_bot.handlers.patient.patient_service import PatientService
from tg_bot.keyboards import PatientKeyboard
from tg_bot.blanks import PatientBlank

router = Router()

@router.callback_query(F.data.startswith(PatientAction.CONNECT_TO_DOCTOR))
async def nigger(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[PatientKeyboard],
    blank: type[PatientBlank],
    user_dbm: UserDBM,
):
    page = await PatientService.get_doctor_selection_page(callback_query.data)

    available_doctors = await PatientService.get_available_doctors()

    await MessageService.edith_managed_message(
        bot=callback_query.bot,
        user_id=callback_query.from_user.id,
        text=blank.get_doctor_selection_blank(),
        reply_markup=keyboard.get_doctor_selection_keyboard(doctors=available_doctors, page=page),
        state=state,
        previous_message_key="start_msg_id",
        message_id_storage_key="start_msg_id"
    )
    

@router.callback_query()
async def f(cacallback_query: CallbackQuery):
    cacallback_query.answer(cacallback_query.data)