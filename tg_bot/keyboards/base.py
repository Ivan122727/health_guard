from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_base_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="Помощь"), KeyboardButton(text="Информация")],
        [KeyboardButton(text="Настройки")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True) 