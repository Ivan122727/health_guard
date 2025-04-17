from abc import ABC, abstractmethod
from aiogram.types import InlineKeyboardMarkup

class CommonBlank(ABC):
    @staticmethod
    @abstractmethod
    def get_default_blank(full_name: str) -> str:
        """Абстрактный метод: главное меню (должен быть реализован в каждом классе-наследнике)"""
        pass
    
    @staticmethod
    def get_change_full_name_blank() -> str:
        return (
            "Введите ваше ФИО!\n"
            "Формат ввода: Фамилия Имя Отчество\n"
            "Примечание: Если у вас несколько имен, введите их через дефис!"
        )
