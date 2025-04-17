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
            "✏️ <b>Введите ваше полное ФИО</b>\n\n"
            "📝 <b>Формат ввода:</b>\n"
            "Фамилия Имя Отчество\n\n"
            "💡 <b>Примеры:</b>\n"
            "• Иванов Иван Иванович\n"
            "• Петрова Анна-Мария Сергеевна\n\n"
            "ℹ️ <b>Примечание:</b>\n"
            "Если у вас двойное имя, введите его через дефис!"
        )

    @staticmethod
    def get_success_change_full_name_blank(new_full_name: str) -> str:
        return (
            "✅ <b>Данные успешно обновлены!</b>\n\n"
            f"👤 <b>Ваше новое ФИО в системе:</b>\n"
            f"{new_full_name}"
        )

    @staticmethod
    def get_invalid_name_format_blank() -> str:
        return (
            "⚠️ <b>Некорректный формат ФИО</b>\n\n"
            "Пожалуйста, введите ваше полное имя в формате:\n"
            "<code>Фамилия Имя Отчество</code>\n\n"
            "🔹 Используйте только буквы и дефисы\n"
            "🔹 Минимум 2 слова (Фамилия и Имя)\n"
            "🔹 Максимальная длина - 100 символов"
        )