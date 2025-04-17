from abc import ABC, abstractmethod
from aiogram.types import InlineKeyboardMarkup

class CommonKeyboard(ABC):
    @staticmethod
    @abstractmethod
    def get_default_keyboard() -> InlineKeyboardMarkup:
        """Абстрактный метод: главное меню (должен быть реализован в каждом классе-наследнике)"""
        pass
