import os
import sys
from pathlib import Path

# Получаем путь к родительской директории
parent_dir = Path(__file__).parent.parent
# Добавляем родительскую директорию в PYTHONPATH
sys.path.append(str(parent_dir))
# Устанавливаем текущую рабочую директорию
os.chdir(parent_dir)

from shared.config import DatabaseSettings, AdminSettings, BotSettings, get_cashed_settings

settings = DatabaseSettings()
print(settings.DATABASE_URL)

admin_settings = AdminSettings()
print(admin_settings.ADMIN_USERNAME)

bot_settings = BotSettings()
print(bot_settings.BOT_TOKEN)   


print(get_cashed_settings().database.DATABASE_URL)
print(get_cashed_settings().admin.ADMIN_USERNAME)
print(get_cashed_settings().bot.BOT_TOKEN)