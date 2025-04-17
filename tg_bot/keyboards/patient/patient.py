from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tg_bot.keyboards.common.common import CommonKeyboard
from tg_bot.keyboards.patient.callback_data import PatientAction

class PatientKeyboard(CommonKeyboard):
    @staticmethod
    def get_default_keyboard() -> InlineKeyboardMarkup:
        """Реализация главного меню для пациента"""
        keyboard = InlineKeyboardBuilder()
        
        keyboard.button(text="Изменить ФИО в системе", callback_data=PatientAction.CHANGE_FULL_NAME)
        keyboard.button(text="Закрепиться за доктором", callback_data=PatientAction.CONNECT_TO_DOCTOR)
        
        keyboard.adjust(1)
        
        return keyboard.as_markup()