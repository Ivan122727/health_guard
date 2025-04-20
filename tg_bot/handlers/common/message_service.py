from typing import Any, Optional
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.exceptions import TelegramBadRequest

class MessageService:
    """Класс для управления сообщениями бота с поддержкой FSM."""
    
    @staticmethod
    async def remove_previous_message(
        bot: Bot, 
        user_id: int, 
        message_id: Optional[int] = None
    ) -> None:
        """
        Удаляет указанное сообщение бота у пользователя.
        
        Args:
            bot: Экземпляр бота
            user_id: ID чата пользователя
            message_id: ID сообщения для удаления (опционально)
        """
        if message_id is not None:
            try:
                await bot.delete_message(chat_id=user_id, message_id=message_id)
            except Exception:
                # Сообщение могло быть уже удалено или недоступно
                pass
    
    @staticmethod
    async def edith_previous_message(
        bot: Bot,
        text: str,
        user_id: int,
        message_id: Optional[int] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        state: Optional[FSMContext] = None,
        new_state: Optional[State] = None
    ):
        if message_id:
            try:
                await bot.edit_message_text(
                    text=text,
                    chat_id=user_id,
                    message_id=message_id,
                )
                await bot.edit_message_reply_markup(
                    chat_id=user_id,
                    message_id=message_id,
                    reply_markup=reply_markup
                )
            except Exception as e:
                pass
        if state:
            await state.set_state(new_state)

    @staticmethod
    async def send_managed_message(
        bot: Bot,
        user_id: int,
        text: str,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        state: Optional[FSMContext] = None,
        previous_message_key: Optional[str] = None,
        new_state: Optional[State] = None,
        message_id_storage_key: Optional[str] = None
    ) -> Message:
        """
        Отправляет управляемое сообщение с поддержкой FSM.
        
        Args:
            bot: Экземпляр бота
            user_id: ID чата пользователя
            text: Текст сообщения
            reply_markup: Клавиатура (опционально)
            state: Контекст состояния FSM (опционально)
            previous_message_key: Ключ для удаления предыдущего сообщения (опционально)
            new_state: Новое состояние FSM (опционально)
            message_id_storage_key: Ключ для сохранения ID сообщения (опционально)
            
        Returns:
            Объект отправленного сообщения
        """
        # Удаляем предыдущее сообщение если требуется
        if state and previous_message_key:
            state_data = await state.get_data()
            await MessageService.remove_previous_message(
                bot=bot,
                user_id=user_id,
                message_id=state_data.get(previous_message_key)
            )
        
        # Отправляем новое сообщение
        sent_message = await bot.send_message(
            chat_id=user_id,
            text=text,
            reply_markup=reply_markup
        )
        
        # Обновляем состояние если требуется
        if state:
            if message_id_storage_key:
                await state.update_data({message_id_storage_key: sent_message.message_id})
            
            await state.set_state(new_state)
        
        return sent_message
    
    @staticmethod
    async def edith_managed_message(
        bot: Bot,
        user_id: int,
        text: str,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        state: Optional[FSMContext] = None,
        previous_message_key: Optional[str] = None,
        new_state: Optional[State] = None,
        message_id_storage_key: Optional[str] = None,
        message: Optional[Message] = None
    ) -> Message:
        state_data = await state.get_data()

        if message and state_data.get(previous_message_key) is None:
            await state.update_data({previous_message_key: message.message_id})
            state_data = await state.get_data()

        try:
            if state and state_data.get(previous_message_key):
                message_id = state_data.get(previous_message_key)
                
                await MessageService.edith_previous_message(
                    bot=bot,
                    text=text,
                    user_id=user_id,
                    message_id=message_id,
                    reply_markup=reply_markup,
                    state=state,
                    new_state=new_state
                )
            else:
                await MessageService.send_managed_message(
                    bot=bot,
                    user_id=user_id,
                    text=text,
                    reply_markup=reply_markup,
                    state=state,
                    previous_message_key=previous_message_key,
                    new_state=new_state,
                    message_id_storage_key=message_id_storage_key
                )
        except TelegramBadRequest as e:
            await MessageService.send_managed_message(
                bot=bot,
                user_id=user_id,
                text=text,
                reply_markup=reply_markup,
                state=state,
                previous_message_key=previous_message_key,
                new_state=new_state,
                message_id_storage_key=message_id_storage_key
            )
    
    @staticmethod
    async def set_state_data(
        state: FSMContext, 
        key: str, 
        value: Any
    ) -> None:
        await state.update_data({key: value})
    
    @staticmethod
    async def get_state_data(
        state: FSMContext, 
        key: str, 
    ) -> Any | None:
        state_data = await state.get_data()

        return state_data.get(key)