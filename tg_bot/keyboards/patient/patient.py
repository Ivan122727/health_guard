from dataclasses import dataclass
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List, Optional

from shared.sqlalchemy_db_.sqlalchemy_model import UserDBM
from tg_bot.keyboards.common.common import CommonKeyboard
from tg_bot.keyboards.patient.callback_data import PatientAction

@dataclass
class DoctorPagination:
    page: int = 0
    per_page: int = 10

class PatientKeyboard(CommonKeyboard):
    """Фабрика инлайн-клавиатур для пациента (Factory pattern)"""
    
    @staticmethod
    def get_default_keyboard() -> InlineKeyboardMarkup:
        """Главное меню пациента (Strategy pattern)"""
        builder = InlineKeyboardBuilder()
        
        builder.button(
            text="Изменить ФИО в системе", 
            callback_data=PatientAction.CHANGE_FULL_NAME.value
        )
        builder.button(
            text="Закрепиться за доктором", 
            callback_data=PatientAction.CONNECT_TO_DOCTOR.value
        )
        
        builder.adjust(1)
        return builder.as_markup()
    
    @staticmethod
    def get_doctor_selection_keyboard(
        doctors: List[UserDBM],
        page: int = 0,
        per_page: int = 5
    ) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()
        
        # Добавляем кнопки докторов
        for doctor in doctors[page * per_page : page * per_page + per_page]:
            keyboard.button(
                text=f"👨⚕️ {doctor.full_name}",
                callback_data=f"{PatientAction.SELECT_DOCTOR.value}:{doctor.tg_id}"
            )
        
        if (page * per_page + per_page) < len(doctors):
            keyboard.button(
                text="Следующая страница",
                callback_data=f"{PatientAction.CONNECT_TO_DOCTOR.value}:{page + 1}"
            )
        if (page * per_page - per_page) >= 0:
            keyboard.button(
                text="Предыдущаю страница",
                callback_data=f"{PatientAction.CONNECT_TO_DOCTOR.value}:{page - 1}"
            )

        keyboard.adjust(1)
        return keyboard.as_markup()