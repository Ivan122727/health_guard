import sqlalchemy
from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable
from logging import Logger
from aiogram.types import Message, CallbackQuery

from shared.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from shared.sqlalchemy_db_.sqlalchemy_model import UserDBM
from tg_bot.keyboards.common.factory import KeyboardFactory
from tg_bot.blanks.factory import BlankFactory

class UserActivityMiddleware(BaseMiddleware):
    """
    Middleware для отслеживания активности пользователей.
    - Проверяет наличие пользователя в БД
    - Создаёт нового с ролью пациента, если не найден
    - Добавляет соответствующую клавиатуру в data
    """
    def __init__(self, logger: Logger):
        self.logger = logger

    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        async with get_cached_sqlalchemy_db().new_async_session() as async_session:
            query = await async_session.execute(
                sqlalchemy.select(UserDBM).where(UserDBM.tg_id == event.from_user.id)
            )

            user_dbm = query.scalar_one_or_none()

            if user_dbm is None:
                self.logger.info(f"User was created: {event.from_user.id}")

                user_dbm = UserDBM(
                    tg_id=event.from_user.id,
                    full_name=event.from_user.full_name,
                )
                
                async_session.add(user_dbm)
                await async_session.commit()
                await async_session.refresh(user_dbm)
        
        data["keyboard"] = KeyboardFactory.get(user_dbm.role)
        data["blank"] = BlankFactory.get(user_dbm.role)
        data["user_dbm"] = user_dbm

        action_type = "message" if isinstance(event, Message) else "callback"
        self.logger.info(
            f"User {user_dbm.tg_id} performed {action_type} action: '{event.text if isinstance(event, Message) else event.data}'"
        )
        
        return await handler(event, data) 
    

        