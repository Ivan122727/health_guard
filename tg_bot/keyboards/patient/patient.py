from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List, Optional
from dataclasses import dataclass

from shared.sqlalchemy_db_.sqlalchemy_model import UserDBM
from tg_bot.keyboards.common.common import CommonKeyboard
from tg_bot.keyboards.patient.callback_data import PatientAction

@dataclass
class PaginationConfig:
    items_per_page: int = 5
    current_page: int = 0


class PatientKeyboard(CommonKeyboard):
    """Фабрика инлайн-клавиатур для пациента (Factory pattern)"""
    
    @classmethod
    def get_default_keyboard(cls) -> InlineKeyboardMarkup:
        """Главное меню пациента (Strategy pattern)"""
        builder = InlineKeyboardBuilder()
        
        builder.button(
            text="Изменить ФИО в системе", 
            callback_data=PatientAction.CHANGE_FULL_NAME
        )
        builder.button(
            text="Закрепиться за доктором", 
            callback_data=PatientAction.CONNECT_TO_DOCTOR
        )
        
        builder.adjust(1)
        return builder.as_markup()
    
    @classmethod
    def get_doctor_selection_keyboard(
        cls,
        doctors: List[UserDBM],
        pagination: Optional[PaginationConfig] = None
    ) -> InlineKeyboardMarkup:
        """
        Клавиатура выбора доктора с пагинацией (Builder pattern)
        
        Args:
            doctors: Список доступных докторов
            pagination: Конфигурация пагинации
            
        Returns:
            InlineKeyboardMarkup: Готовая клавиатура
        """
        if not pagination:
            pagination = PaginationConfig()
            
        builder = InlineKeyboardBuilder()
        start_idx = pagination.current_page * pagination.items_per_page
        end_idx = start_idx + pagination.items_per_page
        
        # Добавляем кнопки докторов
        for doctor in doctors[start_idx:end_idx]:
            builder.button(
                text=f"👨⚕️ {doctor.full_name}",
                callback_data=f"{PatientAction.SELECT_DOCTOR}:{doctor.id}"
            )
        
        # Добавляем пагинацию если нужно
        if len(doctors) > pagination.items_per_page:
            cls._add_pagination_controls(builder, doctors, pagination)
        
        builder.adjust(1)
        return builder.as_markup()
    
    @classmethod
    def _add_pagination_controls(
        cls,
        builder: InlineKeyboardBuilder,
        doctors: List[UserDBM],
        pagination: PaginationConfig
    ) -> None:
        """Добавляет элементы управления пагинацией"""
        total_pages = (len(doctors) + pagination.items_per_page - 1) // pagination.items_per_page
        
        if pagination.current_page > 0:
            builder.button(
                text="⬅️ Назад", 
                callback_data=f"{PatientAction.PAGINATE_DOCTORS}:{pagination.current_page - 1}"
            )
        
        builder.button(
            text=f"Страница {pagination.current_page + 1}/{total_pages}",
            callback_data="no_action"
        )
        
        if pagination.current_page < total_pages - 1:
            builder.button(
                text="Вперед ➡️", 
                callback_data=f"{PatientAction.PAGINATE_DOCTORS}:{pagination.current_page + 1}"
            )