from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from tg_bot.keyboards import CommonKeyboard, CommonAction
from tg_bot.blanks import CommonBlank
from tg_bot.handlers.common import MessageService
from tg_bot.handlers.common.user_handler import UserHandler
from shared.sqlalchemy_db_.sqlalchemy_model import UserDBM
from tg_bot.states import ChangeFullNameStates


router = Router()


# Обработчик стартового сообщения
@router.message(State(None))
async def handle_start_message(
    message: Message,
    state: FSMContext,
    keyboard: type[CommonKeyboard],
    blank: type[CommonBlank],
    user_dbm: type[UserDBM]
) -> None:
    """
    Обработка начального сообщения от пользователя
    
    Args:
        message: Входящее сообщение Telegram
        keyboard: Фабрика клавиатур
        blank: Фабрика шаблонов сообщений
    """
    await MessageService.send_managed_message(
        bot=message.bot,
        user_id=message.from_user.id,
        text=blank.get_default_blank(user_dbm.full_name),
        reply_markup=keyboard.get_default_keyboard(),
        state=state,
        previous_message_key="start_msg_id",
        message_id_storage_key="start_msg_id",
    )
    
    # Получаем данные из состояния
    state_data = await state.get_data()
    
    # Удаляем предыдущие служебные сообщения
    await UserHandler._cleanup_previous_message(
        message.bot,
        message.from_user.id,
        state_data.get("start_msg_id")
    )

    # Отправляем стандартное сообщение с клавиатурой
    start_msg = await message.answer(
        text=blank.get_default_blank(user_dbm.full_name),
        reply_markup=keyboard.get_default_keyboard()
    )

    await message.delete()
    await state.update_data(start_msg_id=start_msg.message_id)


# Обработчик запроса на изменение ФИО
@router.callback_query(F.data == CommonAction.CHANGE_FULL_NAME)
async def handle_change_full_name_request(
    callback_query: CallbackQuery,
    state: FSMContext,
    blank: type[CommonBlank],
) -> None:
    """
    Инициализация процесса изменения ФИО
    
    Args:
        callback_query: Входящий callback запрос
        state: Текущее состояние FSM
        keyboard: Фабрика клавиатур
        blank: Фабрика шаблонов сообщений
    """
    # Удаляем предыдущее сообщение
    await callback_query.message.delete()
    
    # Отправляем сообщение с запросом нового ФИО
    change_full_name_msg = await callback_query.message.answer(
        text=blank.get_change_full_name_blank()
    )
    
    # Устанавливаем состояние ожидания нового ФИО
    await state.set_state(ChangeFullNameStates.waiting_new_full_name)
    # Сохраняем ID сообщения для последующего удаления
    await state.update_data(change_full_name_msg_id=change_full_name_msg.message_id)


# Обработчик ввода нового ФИО
@router.message(ChangeFullNameStates.waiting_new_full_name)
async def handle_new_full_name_input(
    message: Message,
    state: FSMContext,
    blank: type[CommonBlank],
    keyboard: type[CommonKeyboard],
) -> None:
    """
    Обработка нового ФИО, введенного пользователем
    
    Args:
        message: Входящее сообщение Telegram с новым ФИО
        state: Текущее состояние FSM
        blank: Фабрика шаблонов сообщений
        keyboard: Фабрика клавиатур
    """
    # Получаем данные из состояния
    state_data = await state.get_data()
    
    # Удаляем предыдущие служебные сообщения
    await UserHandler._cleanup_previous_message(
        message.bot,
        message.from_user.id,
        state_data.get("change_full_name_msg_id")
    )
    if not (await UserHandler.full_name_is_valid(message.text)):
        await message.delete()
        # Отправляем сообщение с запросом нового ФИО
        change_full_name_msg = await message.answer(
            text=blank.get_change_full_name_blank()
        )
        await state.update_data(change_full_name_msg_id=change_full_name_msg.message_id)
        return

    normalized_full_name = await UserHandler._normalize_full_name(message.text)

    # Обновляем ФИО в базе данных
    await UserHandler._update_user_full_name(
        message.from_user.id,
        normalized_full_name
    )
    # Отправляем стартовое сообщение
    await UserHandler._send_start_message(
        message.bot,
        message.from_user.id,
        blank.get_default_blank(normalized_full_name),
        state
    )   
    # Удаляем сообщение пользователя
    await message.delete()