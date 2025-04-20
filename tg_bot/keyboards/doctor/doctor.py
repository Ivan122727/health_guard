from typing import Optional
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tg_bot.handlers.doctor.survey_class import Question
from tg_bot.keyboards.common.common import CommonKeyboard
from tg_bot.keyboards.doctor.callback_data import DoctorAction

class DoctorKeyboard(CommonKeyboard):
    @staticmethod
    def get_default_keyboard() -> InlineKeyboardMarkup:
        """Главное меню врача"""
        keyboard = InlineKeyboardBuilder()
        
        keyboard.button(
            text="✏️ Изменить ФИО в системе", 
            callback_data=DoctorAction.CHANGE_FULL_NAME
        )
        keyboard.button(
            text="📝 Создать опрос", 
            callback_data=DoctorAction.CREATE_TITLE_SURVEY
        )
        keyboard.button(
            text="⏰ Запланировать опрос", 
            callback_data=DoctorAction.SCHEDULE_SURVEY
        )
        keyboard.button(
            text="📋 Получить список вопросов", 
            callback_data=DoctorAction.GET_LIST_QUESTIONS
        )

        keyboard.adjust(1)
        return keyboard.as_markup()
    
    @staticmethod
    def get_question_type_selection_keyboard(
        count_questions: int = 0
    ) -> InlineKeyboardMarkup:
        """Клавиатура выбора типа создаваемого опроса"""
        keyboard = InlineKeyboardBuilder()
        
        if count_questions:
            keyboard.button(
                text="💾 Сохранить опрос",
                callback_data=DoctorAction.SAVE_SURVEY
            )

        keyboard.button(
            text="✏️ Создать новый вопрос (с нуля)",
            callback_data=DoctorAction.CREATE_NEW_QUESTION
        )
        keyboard.button(
            text="📂 Использовать существующий вопрос (по ID)",
            callback_data=DoctorAction.CREATE_TEMPLATE_QUESTION
        )

        keyboard.button(
            text="❌ Отменить создание опроса",
            callback_data=DoctorAction.CANCEL_CREATE_SURVEY
        )

        keyboard.adjust(1)
        return keyboard.as_markup()

    @staticmethod
    def get_confirm_create_new_question_keyboard() -> InlineKeyboardMarkup:
        """Клавиатура подтверждения создания нового опроса"""
        keyboard = InlineKeyboardBuilder()
        
        keyboard.button(
            text="✅ Подтвердить выбор типа вопроса",
            callback_data=DoctorAction.CONFIRM_CREATE_NEW_QUESTION
        )
        keyboard.button(
            text="↩️ К выбору типа вопроса",
            callback_data=DoctorAction.CHOOSE_TYPE_QUESTION
        )

        keyboard.button(
            text="❌ Отменить создание опроса",
            callback_data=DoctorAction.CANCEL_CREATE_SURVEY
        )
        
        keyboard.adjust(1)
        return keyboard.as_markup()
    
    @staticmethod
    def get_confirm_create_template_question_keyboard() -> InlineKeyboardMarkup:
        """Клавиатура подтверждения создания нового опроса"""
        keyboard = InlineKeyboardBuilder()
        
        keyboard.button(
            text="✅ Подтвердить выбор типа вопроса",
            callback_data=DoctorAction.CONFIRM_CREATE_TEMPLATE_QUESTION
        )
        keyboard.button(
            text="↩️ К выбору типа вопроса",
            callback_data=DoctorAction.CHOOSE_TYPE_QUESTION
        )

        keyboard.button(
            text="❌ Отменить создание опроса",
            callback_data=DoctorAction.CANCEL_CREATE_SURVEY
        )
        
        keyboard.adjust(1)
        return keyboard.as_markup()
    

    @staticmethod
    def get_question_management_keyboard(
        count_questions: int = 0
    ) -> InlineKeyboardMarkup:
        """Клавиатура управления созданием опроса"""
        keyboard = InlineKeyboardBuilder()
        
        if count_questions:
            keyboard.button(
                text="💾 Сохранить опрос",
                callback_data=DoctorAction.SAVE_SURVEY
            )

            keyboard.button(
                text="✏️ Редактировать опрос",
                callback_data=DoctorAction.EDIT_SURVEY
            )

        keyboard.button(
            text="❌ Отменить создание опроса",
            callback_data=DoctorAction.CANCEL_CREATE_SURVEY
        )
        
        keyboard.adjust(1)
        return keyboard.as_markup()

    @staticmethod
    def get_edit_survey_keyboard(
        current_question: Optional[Question] = None,
        previout_question: Optional[Question] = None,
        next_question: Optional[Question] = None,
    ) -> InlineKeyboardMarkup:
        """Клавиатура редактирования опроса"""
        keyboard = InlineKeyboardBuilder()
        
        # Основные кнопки редактирования
        keyboard.button(
            text="➕ Добавить вопрос",
            callback_data=DoctorAction.CHOOSE_TYPE_QUESTION
        )
        
        keyboard.button(
            text="✏️ Изменить название",
            callback_data=DoctorAction.EDIT_SURVEY_TITLE
        )

        if current_question:
            keyboard.button(
                text="✏️ Изменить текущий вопрос",
                callback_data=DoctorAction.EDIT_QUESTION
            )
            keyboard.button(
                text="🗑 Удалить текущий вопрос",
                callback_data=DoctorAction.REMOVE_CURRENT_QUESTION
            )
        
        keyboard.button(
            text="❌ Отменить создание",
            callback_data=DoctorAction.CANCEL_CREATE_SURVEY
        )

        if current_question:
            keyboard.button(
                text="✅ Завершить редактирование",
                callback_data=DoctorAction.FINISH_EDITING
            )

            keyboard.button(
                    text="💾 Сохранить опрос",
                    callback_data=DoctorAction.SAVE_SURVEY
            )

            if previout_question:
                keyboard.button(
                    text="◀️ Пред. вопрос",
                    callback_data=f"{DoctorAction.SET_CURRENT_QUESTION.value}:{previout_question.id}"
                )
            if next_question:
                keyboard.button(
                    text="▶️ След. вопрос",
                    callback_data=f"{DoctorAction.SET_CURRENT_QUESTION.value}:{next_question.id}"
                )

        # Настройка расположения кнопок
        keyboard.adjust(2, 1, 2, 2, 2)

        return keyboard.as_markup()
    
    @staticmethod
    def get_survey_title_keyboard() -> InlineKeyboardMarkup:
        """Клавиатура для ввода названия опроса"""
        keyboard = InlineKeyboardBuilder()
        
        keyboard.button(
            text="✅ Подтвердить название",
            callback_data=DoctorAction.CONFIRM_TITLE_SURVEY
        )
        keyboard.button(
            text="✏️ Ввести заново",
            callback_data=DoctorAction.CREATE_TITLE_SURVEY
        )
        keyboard.button(
            text="❌ Отменить создание",
            callback_data=DoctorAction.CANCEL_CREATE_SURVEY
        )
        
        keyboard.adjust(1)
        return keyboard.as_markup()