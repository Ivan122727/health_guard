from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
import sqlalchemy

from shared.sqlalchemy_db_.sqlalchemy_model import UserDBM
from shared.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from tg_bot.keyboards import PatientAction
from tg_bot.handlers.common.message_service import MessageService
from tg_bot.keyboards import PatientKeyboard
from tg_bot.blanks import PatientBlank

patient_router = Router()

@patient_router.callback_query(PatientAction.CONNECT_TO_DOCTOR in F.data)
async def nigger(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[PatientKeyboard],
    blank: type[PatientBlank],
    user_dbm: UserDBM,
):
    async with get_cached_sqlalchemy_db().new_async_session() as async_session:
        
        result = await async_session.execute(
                sqlalchemy.select(UserDBM).where(UserDBM.role == UserDBM.Roles.doctor)
        )
        doctors = result.scalars().unique()

    await MessageService.send_managed_message(
        bot=callback_query.bot,
        user_id=callback_query.from_user.id,
        text=blank.get_doctor_selection_blank(),
        reply_markup=keyboard.get_doctor_selection_keyboard(doctors=doctors),
        state=state,
        previous_message_key="start_msg_id",
        message_id_storage_key="doctor_selection_msg_id"
    )
