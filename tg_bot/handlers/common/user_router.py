from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from tg_bot.keyboards import CommonKeyboard, CommonAction
from tg_bot.blanks import CommonBlank
from tg_bot.handlers.common.message_service import MessageService
from tg_bot.handlers.common.user_service import UserService
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
    await MessageService.edith_managed_message(
        bot=message.bot,
        user_id=message.from_user.id,
        text=blank.get_default_blank(user_dbm.full_name),
        reply_markup=keyboard.get_default_keyboard(),
        state=state,
        previous_message_key="start_msg_id",
        message_id_storage_key="start_msg_id",
    )

    # # Удаляем сообщение пользователя
    # await MessageService.remove_previous_message(
    #     bot=message.bot,
    #     user_id=message.from_user.id,
    #     message_id=message.message_id
    # )


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
    await MessageService.edith_managed_message(
        bot=callback_query.bot,
        user_id=callback_query.from_user.id,
        text=blank.get_change_full_name_blank(),
        state=state,
        previous_message_key="start_msg_id",
        new_state=ChangeFullNameStates.waiting_new_full_name,
        message_id_storage_key="start_msg_id",
    )

    await MessageService.remove_previous_message(
        bot=callback_query.bot,
        user_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id
    )


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
    if await UserService.full_name_is_valid(message.text):
        normalized_full_name = await UserService.normalize_full_name(message.text)
        
        text = blank.get_default_blank(normalized_full_name)
        message_id_storage_key = "start_msg_id"
        reply_markup = keyboard.get_default_keyboard()
        new_state = None

        # Обновляем ФИО в базе данных
        await UserService.update_user_full_name(
            message.from_user.id,
            normalized_full_name
        )
    else:
        text = blank.get_change_full_name_blank()
        message_id_storage_key = "change_full_name_msg_id"
        reply_markup = None
        new_state = ChangeFullNameStates.waiting_new_full_name

    await MessageService.send_managed_message(
        bot=message.bot,
        user_id=message.from_user.id,
        text=text,
        reply_markup=reply_markup,
        state=state,
        previous_message_key="change_full_name_msg_id",
        new_state=new_state,
        message_id_storage_key=message_id_storage_key
    )

    # Удаляем сообщение пользователя
    await MessageService.remove_previous_message(
        bot=message.bot,
        user_id=message.from_user.id,
        message_id=message.message_id
    )