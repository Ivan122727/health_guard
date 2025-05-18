from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List

from shared.sqlalchemy_db_.sqlalchemy_model import UserDBM
from tg_bot.keyboards.common.common import CommonKeyboard
from tg_bot.keyboards.patient.callback_data import PatientAction


class PatientKeyboard(CommonKeyboard):
    """Фабрика инлайн-клавиатур для пациента (Factory pattern)"""
    
    @staticmethod
    def get_default_keyboard() -> InlineKeyboardMarkup:
        """Главное меню пациента (Strategy pattern)"""
        keyboard = InlineKeyboardBuilder()
        
        keyboard.button(
            text="✏️ Изменить ФИО в системе", 
            callback_data=PatientAction.CHANGE_FULL_NAME.value
        )
        keyboard.button(
            text="👨⚕️ Закрепиться за доктором", 
            callback_data=PatientAction.CONNECT_TO_DOCTOR.value
        )
        
        keyboard.adjust(1)
        return keyboard.as_markup()
    
    @staticmethod
    def get_doctor_selection_keyboard(
        doctors: List[UserDBM],
        page: int = 0,
        per_page: int = 5
    ) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()
        
        # Добавляем кнопки докторов (каждая в отдельную строку)
        for doctor in doctors[page * per_page : page * per_page + per_page]:
            keyboard.button(
                text=f"👨⚕️ {doctor.full_name}",
                callback_data=f"{PatientAction.SELECT_DOCTOR.value}:{doctor.tg_id}"
            )
            keyboard.adjust(1)  # Каждый доктор на новой строке
        
        # Кнопки пагинации в одной строке
        pagination_buttons = []
        
        if (page * per_page - per_page) >= 0:
            pagination_buttons.append((
                "⬅️ Назад",
                f"{PatientAction.CONNECT_TO_DOCTOR.value}:{page - 1}"
            ))
            
        if (page * per_page + per_page) < len(doctors):
            pagination_buttons.append((
                "Вперёд ➡️",
                f"{PatientAction.CONNECT_TO_DOCTOR.value}:{page + 1}"
            ))
        
        # Добавляем кнопки пагинации
        for text, callback_data in pagination_buttons:
            keyboard.button(text=text, callback_data=callback_data)
        
        # Настраиваем layout: доктора по 1, пагинацию в 1 или 2 кнопки в строке
        if len(pagination_buttons) == 2:
            keyboard.adjust(*[1]*per_page, 2)  # Все доктора по 1, пагинация 2 в ряд
        else:
            keyboard.adjust(*[1]*(per_page + 1))  # Все элементы по 1 в ряд
            
        return keyboard.as_markup()
    
    @staticmethod
    def get_selected_doctor_keyboard(
        doctor_id: int
    ) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()

        keyboard.button(
            text="✅ Подтвердить выбор", 
            callback_data=f"{PatientAction.CONFIRM_SELECTED_DOCTOR.value}:{doctor_id}"
        )
        keyboard.button(
            text="🔄 Выбрать другого доктора", 
            callback_data=PatientAction.CONNECT_TO_DOCTOR.value
        )
        keyboard.button(
            text="❌ Отмена", 
            callback_data=PatientAction.CANCEL_CONNECT_TO_DOCTOR.value
        )

        keyboard.adjust(1)
        return keyboard.as_markup()
    
    @staticmethod
    def get_survey_notification_keyboard(
        notification_id: int,
    ) -> InlineKeyboardMarkup:
        """
        Клавиатура для уведомления о необходимости пройти опрос
        
        Args:
            notification_id: ID уведомления об опросе
            can_postpone: Можно ли отложить опрос
            
        Returns:
            InlineKeyboardMarkup: Клавиатура с кнопками действий
        """
        keyboard = InlineKeyboardBuilder()
        
        # Основная кнопка начала опроса
        keyboard.button(
            text="▶️ Начать опрос",
            callback_data=f"{PatientAction.START_SURVEY.value}:{notification_id}"
        )
        
        keyboard.adjust(1)
        return keyboard.as_markup()
    
    @staticmethod
    def get_survey_question_keyboard(
        question_id: int,
        options: List[str],
        has_previous: bool = False
    ) -> InlineKeyboardMarkup:
        """
        Клавиатура с вариантами ответов на вопрос опроса
        
        Args:
            question_id: ID текущего вопроса
            options: Список вариантов ответа
            has_previous: Есть ли предыдущий вопрос для возврата
            
        Returns:
            InlineKeyboardMarkup: Клавиатура с кнопками ответов
        """
        keyboard = InlineKeyboardBuilder()
        
        # Кнопки вариантов ответа (каждая в отдельной строке)
        for i, option in enumerate(options, start=1):
            keyboard.button(
                text=f"{i}. {option}",
                callback_data=f"{PatientAction.ANSWER_QUESTION.value}:{question_id}:{i}"
            )
        
        # Кнопка "Предыдущий вопрос" (если нужно)
        if has_previous:
            keyboard.button(
                text="◀️ Предыдущий вопрос",
                callback_data=f"{PatientAction.PREV_QUESTION.value}:{question_id}"
            )
        
        # Настраиваем layout: каждый вариант ответа на новой строке, 
        # кнопка "назад" внизу отдельно
        keyboard.adjust(*[1]*len(options), 1)
        
        return keyboard.as_markup()