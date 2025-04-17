from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tg_bot.keyboards.common.common import CommonKeyboard
from tg_bot.keyboards.doctor.callback_data import DoctorAction

class DoctorKeyboard(CommonKeyboard):
    @staticmethod
    def get_default_keyboard() -> InlineKeyboardMarkup:
        """Реализация главного меню для пациента"""
        keyboard = InlineKeyboardBuilder()
        
        keyboard.button(text="Изменить ФИО в системе", callback_data=DoctorAction.CHANGE_FULL_NAME)
        keyboard.button(text="Создать опрос", callback_data=DoctorAction.CREATE_SURVEY)
        keyboard.button(text="Запланировать опрос", callback_data=DoctorAction.SCHEDULE_SURVEY)
        keyboard.button(text="Получить список вопросов", callback_data=DoctorAction.GET_LIST_QUESTIONS)

        keyboard.adjust(1)
        
        return keyboard.as_markup()