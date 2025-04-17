from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
import sqlalchemy

from tg_bot.keyboards import CommonKeyboard, CommonAction
from tg_bot.blanks import CommonBlank
from tg_bot.states import ChangeFullNameStates
from tg_bot.utils import validate_and_normalize_full_name

from shared.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from shared.sqlalchemy_db_.sqlalchemy_model import UserDBM

router = Router(name="user_router")


@router.message(State(None))
async def start_message_handler(
    message: Message, 
    state: FSMContext,
    keyboard: type[CommonKeyboard],
    blank: type[CommonBlank]
):
    await message.answer(text=blank.get_default_blank(), reply_markup=keyboard.get_default_keyboard())
    await message.delete()


@router.callback_query(F.data == CommonAction.CHANGE_FULL_NAME)
async def change_full_name_handler(
        callback_query: CallbackQuery,
        state: FSMContext,
        keyboard: type[CommonKeyboard],
        blank: type[CommonBlank],
):
    change_full_name_msg = await callback_query.message.answer(text=blank.get_change_full_name_blank())
    await callback_query.message.delete()

    await state.set_state(ChangeFullNameStates.waiting_new_full_name)
    await state.update_data(change_full_name_msg=change_full_name_msg)


@router.message(ChangeFullNameStates.waiting_new_full_name)
async def apply_new_full_name_handler(
    message: Message,
    state: FSMContext,
    blank: type[CommonBlank],
    keyboard: type[CommonKeyboard],
):
    change_full_name_msg = await state.get_value("change_full_name_msg")
    try:
        if change_full_name_msg:
            await message.bot.delete_message(
                chat_id=message.from_user.id, 
                message_id=change_full_name_msg.message_id
            )
    except Exception as e:
        pass

    try:
        normalized_full_name = validate_and_normalize_full_name(message.text)
        await message.answer(text=blank.get_default_blank(), reply_markup=keyboard.get_default_keyboard())
        
        async with get_cached_sqlalchemy_db().new_async_session() as async_session:
            query = await async_session.execute(
                sqlalchemy.select(UserDBM).where(UserDBM.tg_id == message.from_user.id)
            )

            user_dbm = query.scalar_one()
            user_dbm.full_name = normalized_full_name
            await async_session.commit()
        
        await state.clear()
    except ValueError as e:
        pass

    await message.delete()
        