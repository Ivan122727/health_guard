from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

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
            callback_data=DoctorAction.CREATE_SURVEY
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
    def get_survey_type_selection_keyboard() -> InlineKeyboardMarkup:
        """Клавиатура выбора типа создаваемого опроса"""
        keyboard = InlineKeyboardBuilder()
        
        keyboard.button(
            text="✏️ Создать новый опрос (с нуля)",
            callback_data=DoctorAction.CREATE_NEW_SURVEY
        )
        keyboard.button(
            text="📂 Использовать шаблон (по ID)",
            callback_data=DoctorAction.CREATE_TEMPLATE_SURVEY
        )
        # keyboard.button(
        #     text="⬅️ Назад",
        #     callback_data=DoctorAction.BACK_TO_MENU
        # )

        keyboard.adjust(1)
        return keyboard.as_markup()

    @staticmethod
    def get_back_to_survey_type_keyboard() -> InlineKeyboardMarkup:
        """Клавиатура с кнопкой возврата к выбору типа опроса"""
        keyboard = InlineKeyboardBuilder()
        keyboard.button(
            text="↩️ К выбору типа опроса",
            callback_data=DoctorAction.CREATE_SURVEY
        )
        return keyboard.as_markup()
    
    @staticmethod
    def get_confirm_create_new_survey_keyboard() -> InlineKeyboardMarkup:
        """Клавиатура подтверждения создания нового опроса"""
        keyboard = InlineKeyboardBuilder()
        
        keyboard.button(
            text="✅ Подтвердить выбор типа для создания",
            callback_data=DoctorAction.CONFIRM_CREATE_NEW_SURVEY
        )
        keyboard.button(
            text="↩️ К выбору типа опроса",
            callback_data=DoctorAction.CREATE_SURVEY
        )
        
        keyboard.adjust(1)
        return keyboard.as_markup()
    
    @staticmethod
    def get_confirm_create_template_survey_keyboard() -> InlineKeyboardMarkup:
        """Клавиатура подтверждения создания нового опроса"""
        keyboard = InlineKeyboardBuilder()
        
        keyboard.button(
            text="✅ Подтвердить выбор типа для создания",
            callback_data=DoctorAction.CONFIRM_CREATE_TEMPLATE_SURVEY
        )
        keyboard.button(
            text="↩️ К выбору типа опроса",
            callback_data=DoctorAction.CREATE_SURVEY
        )
        
        keyboard.adjust(1)
        return keyboard.as_markup()
    

    @staticmethod
    def get_survey_management_keyboard() -> InlineKeyboardMarkup:
        """Клавиатура управления созданием опроса"""
        keyboard = InlineKeyboardBuilder()
        
        keyboard.button(
            text="💾 Сохранить опрос",
            callback_data=DoctorAction.SAVE_SURVEY
        )
        keyboard.button(
            text="✏️ Редактировать опрос",
            callback_data=DoctorAction.EDITH_SURVEY
        )
        keyboard.button(
            text="❌ Отменить создание",
            callback_data=DoctorAction.CANCEL_CREATE_SURVEY
        )
        # keyboard.button(
        #     text="⬅️ В главное меню",
        #     callback_data=DoctorAction.BACK_TO_MENU
        # )
        
        keyboard.adjust(1)
        return keyboard.as_markup()

    @staticmethod
    def get_edit_survey_keyboard() -> InlineKeyboardMarkup:
        """Клавиатура редактирования опроса"""
        keyboard = InlineKeyboardBuilder()
        
        keyboard.button(
            text="➕ Добавить вопрос",
            callback_data=DoctorAction.ADD_QUESTION
        )
        keyboard.button(
            text="✏️ Изменить вопрос",
            callback_data=DoctorAction.EDIT_QUESTION
        )
        keyboard.button(
            text="🗑 Удалить вопрос",
            callback_data=DoctorAction.DELETE_QUESTION
        )
        keyboard.button(
            text="✅ Завершить редактирование",
            callback_data=DoctorAction.FINISH_EDITING
        )
        
        keyboard.adjust(2, 2)
        return keyboard.as_markup()