import logging
import os
from pathlib import Path
import sys
from aiogram import Bot, Dispatcher
from aiogram.methods import DeleteWebhook
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

# Получаем путь к родительской директории
parent_dir = Path(__file__).parent.parent
# Добавляем родительскую директорию в PYTHONPATH
sys.path.append(str(parent_dir))
# Устанавливаем текущую рабочую директорию
os.chdir(parent_dir)

from shared.config import BotSettings
from tg_bot.middlewares.user_activity import UserActivityMiddleware
from tg_bot.handlers.base import router

class LoggerConfig:
    """Класс для настройки логгера (Singleton)"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._setup_logging()
        return cls._instance
    
    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)

class BotInitializer:
    """Класс для инициализации бота (Factory)"""
    def __init__(self, settings: BotSettings):
        self.settings = settings
        self.logger = LoggerConfig().logger
        self.bot = self._create_bot()
        self.dp = self._create_dispatcher()

    def _create_bot(self) -> Bot:
        return Bot(
            token=self.settings.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )

    def _create_dispatcher(self) -> Dispatcher:
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)
        self._setup_middleware(dp)
        self._setup_routers(dp)
        return dp

    def _setup_middleware(self, dp: Dispatcher):
        """Настройка middleware (Strategy pattern)"""
        activity_middleware = UserActivityMiddleware(logger=self.logger)
        dp.message.middleware(activity_middleware)
        dp.callback_query.middleware(activity_middleware)

    def _setup_routers(self, dp: Dispatcher):
        dp.include_routers(router)

    async def start(self):
        """Запуск бота"""
        await self.bot(DeleteWebhook(drop_pending_updates=True))
        
        for admin_id in self.settings.ADMIN_IDS:
            await self.bot.send_message(
                chat_id=admin_id,
                text="Бот запущен!"
            )
            
        self.logger.info("Bot started successfully")
        await self.dp.start_polling(self.bot)

def start_bot():
    """Точка входа в приложение"""
    bot_settings = BotSettings()
    bot_initializer = BotInitializer(settings=bot_settings)
    
    import asyncio
    asyncio.run(bot_initializer.start())

if __name__ == "__main__":
    start_bot()