import sqlalchemy

from shared.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from shared.sqlalchemy_db_.sqlalchemy_model import UserDBM
from tg_bot.handlers.common import MessageService
from tg_bot.utils import validate_and_normalize_full_name


class UserHandler(MessageService):
    """Класс для обработки операций, связанных с пользователем"""
    
    @staticmethod
    async def _update_user_full_name(
        user_id: int,
        new_full_name: str
    ) -> None:
        """
        Обновление ФИО пользователя в базе данных
        
        Args:
            user_id: ID пользователя в Telegram
            new_full_name: Новое ФИО пользователя
        """
        async with get_cached_sqlalchemy_db().new_async_session() as async_session:
            result = await async_session.execute(
                sqlalchemy.select(UserDBM).where(UserDBM.tg_id == user_id)
            )
            user = result.scalar_one()  # Получаем одного пользователя
            user.full_name = new_full_name  # Обновляем ФИО
            await async_session.commit()  # Сохраняем изменения

    @staticmethod
    async def full_name_is_valid(full_name: str) -> bool:
        try:
            validate_and_normalize_full_name(full_name)
            return True
        except ValueError:
            return False

    @staticmethod
    async def _normalize_full_name(full_name: str) -> str:
        return validate_and_normalize_full_name(full_name)