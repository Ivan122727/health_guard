from typing import Optional
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from shared.sqlalchemy_db_.sqlalchemy_model.survey import SurveyDBM, UserDBM
from tg_bot.handlers.doctor.survey_models import Question
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
    
    """Создание опроса"""

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
            text="❌ Отменить создание опроса",
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
            text="❌ Отменить создание опроса",
            callback_data=DoctorAction.CANCEL_CREATE_SURVEY
        )
        
        keyboard.adjust(1)
        return keyboard.as_markup()

    """Планирование опроса"""

    @staticmethod
    def get_survey_schedule_type_keyboard() -> InlineKeyboardMarkup:
        """Клавиатура выбора типа расписания опроса"""
        keyboard = InlineKeyboardBuilder()
        
        keyboard.button(
            text="🔄 Несколько раз в день",
            callback_data=DoctorAction.CHOOSE_MULTIPLE_TIMES_PER_DAY
        )
        keyboard.button(
            text="☀️ Раз в день",
            callback_data=DoctorAction.CHOOSE_ONCE_PER_DAY
        )
        keyboard.button(
            text="📆 Раз в несколько дней",
            callback_data=DoctorAction.CHOOSE_EVERY_FEW_DAYS
        )
        keyboard.button(
            text="❌ Отменить планирование",
            callback_data=DoctorAction.CANCEL_SCHEDULING
        )
        
        keyboard.adjust(1)
        return keyboard.as_markup()

    @staticmethod
    def get_multiple_times_per_day_keyboard(flag: bool = True) -> InlineKeyboardMarkup:
        """Клавиатура выбора количества опросов в день"""
        keyboard = InlineKeyboardBuilder()
        if flag:
            for i in range(1, 6):
                keyboard.button(
                    text=f"{i} раз{'а' if 2 <= i <=4 else ''} в день",
                    callback_data=f"{DoctorAction.SET_TIMES_PER_DAY.value}:{i}"
                )
            
        keyboard.button(
            text="↩️ Назад к выбору типа",
            callback_data=DoctorAction.SCHEDULE_SURVEY
        )
        keyboard.button(
            text="❌ Отменить планирование",
            callback_data=DoctorAction.CANCEL_SCHEDULING
        )
        
        keyboard.adjust(2, 2, 1, 1)
        return keyboard.as_markup()

    @staticmethod
    def get_schedule_confirmation_keyboard() -> InlineKeyboardMarkup:
        """Клавиатура подтверждения расписания"""
        keyboard = InlineKeyboardBuilder()
        
        keyboard.button(
            text="✅ Подтвердить расписание",
            callback_data=DoctorAction.CONFIRM_SCHEDULE
        )
        keyboard.button(
            text="✏️ Изменить параметры",
            callback_data=DoctorAction.SCHEDULE_SURVEY
        )
        keyboard.button(
            text="❌ Отменить планирование",
            callback_data=DoctorAction.CANCEL_SCHEDULING
        )
        
        keyboard.adjust(1)
        return keyboard.as_markup()

    @staticmethod
    def get_back_to_schedule_type_keyboard() -> InlineKeyboardMarkup:
        """Клавиатура возврата к выбору типа расписания"""
        keyboard = InlineKeyboardBuilder()
        
        keyboard.button(
            text="↩️ Назад к выбору типа",
            callback_data=DoctorAction.SCHEDULE_SURVEY
        )
        keyboard.button(
            text="❌ Отменить планирование",
            callback_data=DoctorAction.CANCEL_SCHEDULING
        )
        
        keyboard.adjust(1)
        return keyboard.as_markup()

    @staticmethod
    def get_every_few_days_keyboard() -> InlineKeyboardMarkup:
        """Клавиатура выбора интервала в днях"""
        keyboard = InlineKeyboardBuilder()
        
        # Кнопки выбора интервала (1-5 дней)
        intervals = {
            1: "день",
            2: "дня",
            3: "дня",
            4: "дня",
            5: "дней"
        }
        
        for days in range(1, 6):
            keyboard.button(
                text=f"Раз в {days} {intervals[days]}",
                callback_data=f"{DoctorAction.SET_INTERVAL_DAYS.value}:{days}"
            )
        
        # Кнопки навигации
        keyboard.button(
            text="↩️ Назад к выбору типа",
            callback_data=DoctorAction.SCHEDULE_SURVEY
        )
        keyboard.button(
            text="❌ Отменить планирование",
            callback_data=DoctorAction.CANCEL_SCHEDULING
        )
        
        # Расположение кнопок (первые 5 - выбор интервала, затем навигация)
        keyboard.adjust(2, 2, 1, 2)
        return keyboard.as_markup()

    @staticmethod
    def get_date_period_keyboard(
        has_both_dates: bool = False
    ):
        keyboard = InlineKeyboardBuilder()
        
        keyboard.button(
            text="↩️ Назад к выбору типа",
            callback_data=DoctorAction.SCHEDULE_SURVEY
        )
        keyboard.button(
            text="❌ Отменить планирование",
            callback_data=DoctorAction.CANCEL_SCHEDULING
        )

        if has_both_dates:
            keyboard.button(
                text="✅ Сохранить период",
                callback_data=DoctorAction.CONFIRM_DATE_PERIOD
            )
        keyboard.adjust(2, 1)
        return keyboard.as_markup()
    
    @staticmethod
    def get_survey_selection_keyboard(
        survey_dbms: list[SurveyDBM],
        page: int = 0,
        per_page: int = 5
    ) -> InlineKeyboardMarkup:
        """Клавиатура выбора опроса с пагинацией
        
        Args:
            surveys: Полный список опросов
            page: Текущая страница (начиная с 0)
            per_page: Количество опросов на странице
        """
        keyboard = InlineKeyboardBuilder()
        
        # Добавляем кнопки опросов (каждая в отдельную строку)
        for survey in survey_dbms[page * per_page : page * per_page + per_page]:
            keyboard.button(
                text=f"📋 {survey.title} (ID: {survey.id})",
                callback_data=f"{DoctorAction.SELECT_SURVEY.value}:{survey.id}"
            )
            keyboard.adjust(1)  # Каждый опрос на новой строке
        
        # Кнопки пагинации в одной строке
        pagination_buttons = []
        
        if (page * per_page - per_page) >= 0:
            pagination_buttons.append((
                "⬅️ Назад",
                f"{DoctorAction.CONFIRM_DATE_PERIOD.value}:{page - 1}"
            ))
            
        if (page * per_page + per_page) < len(survey_dbms):
            pagination_buttons.append((
                "Вперёд ➡️",
                f"{DoctorAction.CONFIRM_DATE_PERIOD.value}:{page + 1}"
            ))
        
        # Добавляем кнопки пагинации
        for text, callback_data in pagination_buttons:
            keyboard.button(text=text, callback_data=callback_data)
        
        # Кнопки управления
        keyboard.button(
            text="❌ Отменить планирование",
            callback_data=DoctorAction.CANCEL_SCHEDULING
        )
        
        # Настраиваем layout
        if len(pagination_buttons) == 2:
            keyboard.adjust(*[1]*per_page, 2, 1)  # Опросы по 1, пагинация 2 в ряд, назад внизу
        else:
            keyboard.adjust(*[1]*(per_page + len(pagination_buttons) + 1))  # Все по 1 в ряд
        
        return keyboard.as_markup()

    @staticmethod
    def get_survey_confirmation_keyboard(survey_id: int) -> InlineKeyboardMarkup:
        """Клавиатура подтверждения выбранного опроса для планирования
        
        Args:
            survey_id: ID выбранного опроса
        """
        keyboard = InlineKeyboardBuilder()
        
        # Основные кнопки
        keyboard.button(
            text="✅ Подтвердить выбор",
            callback_data=DoctorAction.CONFIRM_SURVEY_SELECTION.value
        )
        keyboard.button(
            text="🔄 Выбрать другой опрос",
            callback_data=DoctorAction.CONFIRM_DATE_PERIOD
        )
        keyboard.button(
            text="❌ Отменить планирование",
            callback_data=DoctorAction.CANCEL_SCHEDULING
        )
        
        # Расположение кнопок (все в один столбец)
        keyboard.adjust(1)
        return keyboard.as_markup()

    @staticmethod
    def get_patient_selection_keyboard(
        patients_dbms: list[UserDBM],
        page: int = 0,
        per_page: int = 5
    ) -> InlineKeyboardMarkup:
        """Клавиатура выбора пациента с пагинацией
        
        Args:
            patients_dbms: Список пациентов
            page: Текущая страница (начиная с 0)
            per_page: Количество пациентов на странице
        """
        keyboard = InlineKeyboardBuilder()
        
        # Добавляем кнопки пациентов (каждая в отдельную строку)
        for patient_dbm in patients_dbms[page * per_page : page * per_page + per_page]:
            keyboard.button(
                text=f"👤 {patient_dbm.full_name}",
                callback_data=f"{DoctorAction.SELECT_PATIENT.value}:{patient_dbm.tg_id}"
            )
        
        # Кнопки пагинации
        pagination_buttons = []
        if (page * per_page - per_page) >= 0:
            pagination_buttons.append((
                "⬅️ Назад",
                f"{DoctorAction.CONFIRM_SURVEY_SELECTION.value}:{page - 1}"
            ))
            
        if (page * per_page + per_page) < len(patients_dbms):
            pagination_buttons.append((
                "Вперёд ➡️",
                f"{DoctorAction.CONFIRM_SURVEY_SELECTION.value}:{page + 1}"
            ))
        
        # Управляющие кнопки
        keyboard.button(
            text="🔄 Выбрать другой опрос",
            callback_data=DoctorAction.CONFIRM_DATE_PERIOD
        )
        keyboard.button(
            text="❌ Отменить планирование",
            callback_data=DoctorAction.CANCEL_SCHEDULING
        )
        
        # Оптимальное расположение кнопок:
        # 1. Все пациенты по одному в строке (adjust(1) для каждого)
        # 2. Пагинация в одну строку (если есть обе кнопки)
        # 3. Управляющие кнопки в одну строку
        
        # Добавляем пагинацию
        for text, callback_data in pagination_buttons:
            keyboard.button(text=text, callback_data=callback_data)
        
        # Настройка расположения:
        if len(pagination_buttons) == 2:
            # Если есть обе кнопки пагинации
            keyboard.adjust(*[1]*per_page, 2, 2)  # Пациенты по 1, пагинация 2 в ряд, управление 2 в ряд
        elif len(pagination_buttons) == 1:
            # Если только одна кнопка пагинации
            keyboard.adjust(*[1]*per_page, 1, 2)  # Пациенты по 1, пагинация 1, управление 2 в ряд
        else:
            # Нет кнопок пагинации
            keyboard.adjust(*[1]*per_page, 2)  # Пациенты по 1, управление 2 в ряд
        
        return keyboard.as_markup()


    @staticmethod
    def get_patient_confirmation_keyboard(
        patient_dbm: UserDBM,
        add_contact_button: bool = True
    ) -> InlineKeyboardMarkup:
        """Клавиатура подтверждения выбора пациента
        
        Args:
            patient_dbm: Объект пациента (UserDBM)
            survey_id: ID выбранного опроса
        """
        keyboard = InlineKeyboardBuilder()
        
        # Основные кнопки подтверждения
        keyboard.button(
            text="✅ Подтвердить выбор",
            callback_data=DoctorAction.CONFIRM_SELECTED_PATIENT
        )
        keyboard.button(
            text="🔄 Выбрать другого пациента",
            callback_data=DoctorAction.CONFIRM_SURVEY_SELECTION,
        )
        keyboard.button(
            text="📋 Выбрать другой опрос",
            callback_data=DoctorAction.CONFIRM_DATE_PERIOD
        )
        keyboard.button(
            text="❌ Отменить планирование",
            callback_data=DoctorAction.CANCEL_SCHEDULING
        )
        if add_contact_button:
            # Дополнительные кнопки
            keyboard.button(
                text="📞 Связаться с пациентом",
                url=f"tg://user?id={patient_dbm.tg_id}"
            )
        # Расположение кнопок (2 в ряд для основных, 1 для дополнительных)
        keyboard.adjust(2, 2, 1)
        return keyboard.as_markup()