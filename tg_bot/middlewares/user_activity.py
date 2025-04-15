from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Awaitable
import logging

class UserActivityMiddleware(BaseMiddleware):
    """
    Middleware для отслеживания активности пользователей.
    Реализует паттерн Observer для мониторинга действий пользователей.
    """
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id

        # TODO: добавить проверку на наличие пользователя в базе    
        
        action_type = "message" if isinstance(event, Message) else "callback"
        
        self.logger.info(
            f"User {user_id} performed {action_type} action: '{event.text if isinstance(event, Message) else event.data}'"
        )
        
        return await handler(event, data) 