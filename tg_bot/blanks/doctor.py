from datetime import datetime, timedelta
from typing import Optional
from shared.sqlalchemy_db_.sqlalchemy_model import SurveyDBM, UserDBM
from shared.sqlalchemy_db_.sqlalchemy_model.scheduled_survey import ScheduledSurveyDBM
from tg_bot.blanks import CommonBlank
from tg_bot.handlers.doctor.survey_models import Question, Survey


class DoctorBlank(CommonBlank):
    STATE_QUESTION_TEXT = "enter_question"
    STATE_QUESTION_OPTIONS = "enter_options"

    @staticmethod
    def get_default_blank(full_name: str) -> str:
        """Реализация главного меню для доктора"""
        text = (
            f"👨⚕️ <b>Добро пожаловать в MedSurvey Bot!</b> 👩⚕️\n\n"
            f"📋 <b>Ваш профиль</b>\n"
            f"🆔 <b>ФИО в системе:</b> <code>{full_name}</code>\n\n"
            f"🛠 <i>Используйте меню для работы с системой</i>"
        )
        return text

    @staticmethod
    def get_patient_list_blank(patients_count: int) -> str:
        """Сообщение со списком пациентов"""
        return (
            f"👥 <b>Список ваших пациентов</b>\n\n"
            f"📊 <b>Всего пациентов:</b> {patients_count}\n\n"
            f"👇 <i>Выберите пациента из списка ниже</i>"
        )

    @staticmethod
    def get_no_patients_blank() -> str:
        """Сообщение когда нет пациентов"""
        return (
            "😔 <b>У вас пока нет пациентов</b>\n\n"
            "ℹ️ Пациенты смогут прикрепляться к вам через бота\n\n"
            "🔄 <i>Попробуйте проверить позже</i>"
        )

    """Создание опроса"""

    @staticmethod
    def get_survey_title_input_blank() -> str:
        """Сообщение с запросом названия опроса"""
        return (
            "📝 <b>Дайте название вашему опросу</b>\n\n"
            "✏️ <b>Требования к названию:</b>\n"
            "• Должно отражать суть опроса\n"
            "• Не длиннее 100 символов\n"
            "• Без специальных символов (@, #, $ и т.д.)\n\n"
            "📌 <b>Примеры названий:</b>\n"
            "<code> Оценка состояния здоровья</code>\n"
            "<code> Анкета о качестве сна</code>\n"
            "<code> Опрос о физической активности</code>\n\n"
            "👇 <b>Введите название опроса:</b>"
        )

    @staticmethod
    def get_survey_title_confirmation_blank(title: str) -> str:
        """Сообщение с подтверждением введенного названия"""
        return (
            "🔍 <b>Проверьте введенное название:</b>\n\n"
            f"📌 <b>Название опроса:</b>\n<code>{title}</code>\n\n"
            "ℹ️ <i>Если всё верно - подтвердите, либо введите заново</i>\n\n"
            "👇 <b>Выберите действие:</b>"
        )

    @staticmethod
    def get_choose_type_survey_blank() -> str:
        """Сообщение с выбором типа создаваемого опроса"""
        return (
            "📝 <b>Выберите тип создаваемого вопроса:</b>\n\n"
            "1. ✏️ <b>Создать с нуля</b>\n"
            "   • Вы самостоятельно вводите все вопросы\n"
            "   • Полный контроль над структурой опроса\n\n"
            "2. 🔍 <b>Использовать шаблон</b>\n"
            "   • Введите ID из общего списка вопросов\n"
            "   • Быстрое создание на основе готовых шаблонов\n\n"
            "👇 <i>Выберите вариант ниже</i>"
        )

    @staticmethod
    def get_create_from_scratch_blank(step: str = None, current_question: str = None, count_questions: int = 0) -> str:
        """Инструкция для создания опроса с нуля"""
        if step == DoctorBlank.STATE_QUESTION_TEXT:
            questions_info = (
                f"📊 В опросе уже {count_questions} вопросов\n\n" 
                if count_questions > 0 
                else "📝 Вы начинаете новый опрос\n\n"
            )
            return (
                f"{questions_info}"
                "✏️ <b>Введите текст вопроса:</b>\n\n"
                "ℹ️ <i>Требования к вопросу:</i>\n"
                "• Должен быть четким и однозначным\n"
                "• Не должен содержать спецсимволы (@, #, $ и т.д.)\n"
                "• Максимальная длина - 200 символов\n\n"
                "📌 <b>Примеры хороших вопросов:</b>\n"
                "<code>• Как часто вы испытываете головную боль?</code>\n"
                "<code>• Оцените качество сна по шкале от 1 до 5</code>\n"
                "<code>• Какие лекарства вы принимаете регулярно?</code>"
            )
        
        elif step == DoctorBlank.STATE_QUESTION_OPTIONS:
            return (
                f"📝 <b>Добавление вариантов ответа</b>\n\n"
                f"❓ <b>Текущий вопрос:</b>\n<code>{current_question}</code>\n\n"
                "ℹ️ <i>Как вводить варианты:</i>\n"
                "1. Каждый вариант с новой строки\n"
                "2. Минимум 2 варианта\n"
                "3. Максимум 10 вариантов\n"
                "4. Варианты должны быть краткими\n\n"
                "📌 <b>Пример правильного ввода:</b>\n"
                "<code>Никогда\n"
                "Редко (1-2 раза в месяц)\n"
                "Иногда (1-2 раза в неделю)\n"
                "Часто (3-5 раз в неделю)\n"
                "Постоянно</code>\n\n"
                "👇 <b>Введите варианты ответов:</b>"
            )
        
        else:
            return (
                "🛠 <b>Создание нового вопроса</b>\n\n"
                "📋 <b>Процесс создания:</b>\n"
                "1. Вводите <b>текст вопроса</b>\n"
                "2. Добавляете <b>варианты ответов</b>\n"
                "3. Повторяете для каждого вопроса\n"
                "4. Сохраняете готовый опрос\n\n"
                f"📌 Сейчас в опросе: {count_questions} вопросов\n\n"
                "👇 <i>Подтвердите выбор типа вопроса</i>"
            )

    @staticmethod
    def get_use_template_blank(is_error: bool = False) -> str:
        """Инструкция для использования шаблона с обработкой ошибок
        
        Args:
            is_error: Флаг ошибки ввода
        """
        base_text = (
            "📋 <b>Использование шаблонного вопроса</b>\n\n"
            "Введите <b>ID вопроса</b> из общего списка:\n"
            "• Можно найти в каталоге вопросов\n"
            "• Или получить у администратора\n\n"
            "🔢 <b>Пример ввода ID:</b>\n"
            "<code>12345</code>\n\n"
        )
        
        if is_error:
            error_text = (
                "❗️ <b>Ошибка:</b> Вопрос с таким ID не найден\n"
                "• Проверьте правильность ввода\n"
                "• Убедитесь, что вопрос существует и доступен вам\n\n"
            )
            return base_text + error_text + "👇 <b>Попробуйте снова:</b>"
        
        return base_text + "👇 <b>Введите ID вопроса:</b>"

    @staticmethod
    def get_question_info(
        question_number: int,
        total_questions: int,
        current_question: Optional[Question] = None,
    ) -> str:
        """Возвращает форматированную информацию о вопросе
        
        Args:
            question_number: Номер текущего вопроса
            total_questions: Общее количество вопросов
            current_question: Текущий вопрос (None если вопросов нет)
        """
        if current_question is None:
            return (
                "📭 <b>Вопросов пока нет</b>\n\n"
                "ℹ️ Вы можете добавить новый вопрос:\n"
                "• ✏️ Создать с нуля\n"
                "• 📋 Использовать шаблон\n\n"
                "👇 Выберите действие в меню"
            )
        
        # Определяем тип вопроса с иконкой
        type_icon = "📋" if current_question.is_from_template else "✏️"
        type_text = "Шаблонный вопрос" if current_question.is_from_template else "Созданный вопрос"
        
        # Добавляем ID шаблона если вопрос шаблонный
        template_info = ""
        if current_question.is_from_template and current_question.template_question_id:
            template_info = f"\n🔖 <b>ID шаблона:</b> <code>{current_question.template_question_id}</code>"
        
        # Форматируем варианты ответов
        formatted_options = "\n".join(
            f"{i+1}. {option}" 
            for i, option in enumerate(current_question.options)
        ) if current_question.options else "ℹ️ Варианты ответа не добавлены"
        
        return (
            f"📊 <b>Вопрос {question_number}/{total_questions}</b>\n"
            f"{type_icon} <b>Тип:</b> {type_text}{template_info}\n\n"
            f"❓ <b>Вопрос:</b>\n"
            f"<code>{current_question.text}</code>\n\n"
            f"📝 <b>Варианты ответов:</b>\n"
            f"{formatted_options}\n\n"
            f"👇 <i>Выберите действие</i>"
        )
    
    """Планирование опроса"""
    
    @staticmethod
    def get_survey_scheduling_blank() -> str:
        """Сообщение с выбором частоты проведения опроса"""
        return (
            "⏰ <b>Планирование частоты опроса</b>\n\n"
            "📅 <b>Выберите как часто пациенты должны проходить этот опрос:</b>\n\n"
            "1. 🔄 <b>Несколько раз в день</b>\n"
            "   • Вы сможете указать точное количество (1-5 раз)\n"
            "   • И настроить время для каждого опроса\n\n"
            "2. ☀️ <b>Раз в день</b>\n"
            "   • Ежедневно в указанное вами время\n\n"
            "3. 📆 <b>Раз в несколько дней</b>\n"
            "   • Вы указываете интервал (2-7 дней)\n\n"
            "🔔 <b>Для всех типов:</b>\n"
            "• Напоминания будут приходить 3 раза в день\n"
            "• В <code>10:00</code>, <code>14:00</code> и <code>17:00</code>\n"
            "• Если опрос не был пройден\n\n"
            "👇 <i>Выберите подходящий вариант ниже</i>"
        )

    @staticmethod
    def get_choose_multiple_times_blank() -> str:
        """Бланк выбора количества опросов в день"""
        return (
            "🔄 <b>Настройка опроса несколько раз в день</b>\n\n"
            "🔢 <b>Выберите количество опросов в день:</b>\n\n"
            "1️⃣ 1 раз в день (с настройкой времени)\n"
            "2️⃣ 2 раза в день (утро/вечер)\n"
            "3️⃣ 3 раза в день (утро/день/вечер)\n"
            "4️⃣ 4 раза в день (каждые 4-5 часов)\n"
            "5️⃣ 5 раза в день (каждые 3 часа)\n\n"
            "ℹ️ <i>После выбора количества вы сможете указать точное время для каждого опроса</i>\n\n"
            "🔔 <b>Напоминания:</b>\n"
            "• Будут приходить в <code>10:00</code>, <code>14:00</code> и <code>17:00</code>\n"
            "• Если какой-то из опросов не был пройден\n\n"
            "👇 <i>Выберите количество опросов в день</i>"
        )
    
    @staticmethod
    def get_set_times_per_day_blank(count: int, error_msg: Optional[str] = None) -> str:
        """Бланк ввода времени для каждого опроса с обработкой ошибок
        
        Args:
            count: Количество опросов в день (1-5)
            error_msg: Сообщение об ошибке (если есть)
        """
        time_examples = {
            1: ["09:00"],
            2: ["09:00", "19:00"],
            3: ["08:00", "13:00", "18:00"],
            4: ["08:00", "12:00", "16:00", "20:00"],
            5: ["07:00", "10:00", "13:00", "16:00", "19:00"]
        }
        
        example_times = "\n".join(f"{i+1}. {time}" for i, time in enumerate(time_examples[count]))
        
        # Формируем сообщение об ошибке (если есть)
        error_section = ""
        if error_msg:
            error_section = (
                "\n\n❗️ <b>Ошибка ввода:</b>\n"
                f"<code>{error_msg}</code>\n"
                "Пожалуйста, попробуйте снова:\n"
            )
        
        return (
            f"⏱ <b>Настройка времени для {count} опросов в день</b>\n"
            f"{error_section}\n"
            "⌚️ <b>Введите время для каждого опроса:</b>\n"
            "• Каждое время с новой строки\n"
            "• Формат: <code>ЧЧ:ММ</code> (24-часовой)\n"
            "• Минимальный интервал - 2 часа между опросами\n\n"
            f"📌 <b>Пример для {count} опросов:</b>\n"
            f"{example_times}\n\n"
            "⚠️ <b>Ограничения:</b>\n"
            "• Первый опрос не раньше 07:00\n"
            "• Последний опрос не позже 22:00\n"
            "• Все времена должны быть в порядке возрастания\n\n"
            "👇 <b>Введите времена через запятую или с новой строки:</b>"
        )

    @staticmethod
    def get_once_per_day_blank(error_msg: Optional[str] = None) -> str:
        """Бланк настройки ежедневного опроса с обработкой ошибок
        
        Args:
            error_msg: Сообщение об ошибке (если есть)
        """
        # Формируем сообщение об ошибке (если есть)
        error_section = ""
        if error_msg:
            error_section = (
                "\n\n❗️ <b>Ошибка ввода:</b>\n"
                f"<code>{error_msg}</code>\n"
                "Пожалуйста, попробуйте снова:\n"
            )
        
        return (
            "🌞 <b>Настройка ежедневного опроса</b>\n"
            f"{error_section}\n"
            "⌚️ <b>Введите время отправки основного опроса:</b>\n"
            "• Формат: <code>ЧЧ:ММ</code> (24-часовой)\n"
            "• Пример: <code>09:30</code>\n\n"
            "⏳ <b>Допустимый диапазон:</b> 07:00 - 22:00\n\n"
            "🔔 <b>Система напоминаний:</b>\n"
            "1. Основной опрос придет в указанное вами время\n"
            "2. Если пациент не пройдет опрос в течение 2 часов:\n"
            "   • Первое напоминание в <code>10:00</code>\n"
            "   • Второе напоминание в <code>14:00</code>\n"
            "   • Третье напоминание в <code>17:00</code>\n\n"
            "ℹ️ <i>Рекомендации по выбору времени:</i>\n"
            "• Учитывайте типичный распорядок дня пациента\n"
            "• Избегайте слишком ранних (до 08:00) и поздних (после 21:00) часов\n"
            "• Оптимальное время - утро или день, когда пациент наиболее активен\n\n"
            "👇 <b>Введите время в указанном формате:</b>"
        )

    @staticmethod
    def get_once_per_day_confirmation_blank(selected_time: str) -> str:
        """Бланк подтверждения времени для ежедневного опроса"""
        return (
            "✅ <b>Проверьте параметры ежедневного опроса</b>\n\n"
            f"⏰ <b>Основное время отправки:</b> <code>{selected_time}</code>\n\n"
            "🔔 <b>Напоминания будут приходить:</b>\n"
            "• Если опрос не пройден в течение 2 часов\n"
            "• В <code>10:00</code>, <code>14:00</code> и <code>17:00</code>\n\n"
            "⚠️ <b>Обратите внимание:</b>\n"
            "• Напоминания прекратятся после прохождения опроса\n"
            "• Если опрос не пройден до 18:00, он считается пропущенным\n\n"
            "👇 <i>Подтвердите или измените время опроса</i>"
        )
    
    @staticmethod
    def get_every_few_days_blank() -> str:
        """Бланк настройки опроса раз в несколько дней"""
        return (
            "📅 <b>Настройка опроса раз в несколько дней</b>\n\n"
            "🔢 <b>Выберите интервал между опросами:</b>\n\n"
            "• Раз в 1 день\n"
            "• Раз в 2 дня\n"
            "• Раз в 3 дня\n"
            "• Раз в 4 дня\n"
            "• Раз в 5 дней\n\n"
            "ℹ️ <i>После выбора интервала нужно будет указать время отправки</i>\n\n"
            "🔔 <b>Система напоминаний:</b>\n"
            "1. Основной опрос придет в выбранное время\n"
            "2. Если опрос не пройден в этот день:\n"
            "   • Первое напоминание в <code>10:00</code>\n"
            "   • Второе напоминание в <code>14:00</code>\n"
            "   • Третье напоминание в <code>17:00</code>\n\n"
            "👇 <i>Выберите интервал из предложенных вариантов</i>"
        )
    
    @staticmethod
    def get_every_few_days_time_blank(days: int, error_msg: Optional[str] = None) -> str:
        """Бланк ввода времени для опроса раз в несколько дней с обработкой ошибок
        
        Args:
            days: Количество дней между опросами
            error_msg: Сообщение об ошибке (если есть)
        """
        day_form = "день" if days == 1 else "дня" if 2 <= days <= 4 else "дней"
        
        # Формируем сообщение об ошибке (если есть)
        error_section = ""
        if error_msg:
            error_section = (
                "\n\n❗️ <b>Ошибка ввода:</b>\n"
                f"<code>{error_msg}</code>\n"
                "Пожалуйста, попробуйте снова:\n"
            )
        
        return (
            f"⏰ <b>Настройка времени для опроса раз в {days} {day_form}</b>\n"
            f"{error_section}\n"
            "⌚️ <b>Введите время отправки опроса:</b>\n"
            "• Формат: <code>ЧЧ:ММ</code> (24-часовой)\n"
            "• Пример: <code>15:30</code>\n\n"
            "⏳ <b>Допустимый диапазон:</b> 07:00 - 22:00\n\n"
            "🔔 <b>Напоминания будут приходить:</b>\n"
            f"• Если опрос не пройден в день отправки\n"
            "• В <code>10:00</code>, <code>14:00</code> и <code>17:00</code>\n\n"
            "👇 <b>Введите время в указанном формате:</b>"
        )

    @staticmethod
    def get_survey_period_blank(
        error_msg: Optional[str] = None,
        current_start_date: Optional[str] = None,
        current_end_date: Optional[str] = None
    ) -> str:
        """Бланк ввода периода действия опроса (требуются обе даты)
        
        Args:
            error_msg: Сообщение об ошибке (если есть)
            current_start_date: Уже введенная начальная дата (если есть)
            current_end_date: Уже введенная конечная дата (если есть)
        """
        # Формируем сообщение об ошибке
        error_section = ""
        if error_msg:
            error_section = (
                "\n\n❗️ <b>Ошибка ввода:</b>\n"
                f"<code>{error_msg}</code>\n"
                "Пожалуйста, введите обе даты снова:\n"
            )
        
        # Инструкция в зависимости от того, какие даты уже введены
        instruction = ""
        if not current_start_date and not current_end_date:
            instruction = "👇 <b>Введите обе даты через дефис (ДД.ММ.ГГГГ-ДД.ММ.ГГГГ):</b>"
        else:
            instruction = "👇 <b>Введите недостающую дату в формате ДД.ММ.ГГГГ:</b>"
        
        return (
            "📅 <b>Настройка периода действия опроса</b>\n"
            f"{error_section}"
            "\n📆 <b>Необходимо ввести обе даты:</b>\n"
            f"• Начало: <code>{current_start_date if current_start_date else 'ожидается ввод'}</code>\n"
            f"• Конец: <code>{current_end_date if current_end_date else 'ожидается ввод'}</code>\n\n"
            "⏳ <b>Требования:</b>\n"
            "• Обе даты обязательны для ввода\n"
            "• Формат: ДД.ММ.ГГГГ\n"
            "• Дата начала не может быть раньше сегодня\n"
            "• Дата окончания должна быть после начала\n\n"
            "📌 <b>Пример:</b>\n"
            "<code>15.08.2023-30.08.2023</code> (обе даты сразу)\n\n"
            f"{instruction}"
        )
    

    @staticmethod
    def get_survey_selection_blank(has_surveys: bool = False) -> str:
        """Бланк выбора опроса с inline-кнопками
        
        Args:
            surveys: Список опросов формата:
                [{
                    'id': int, 
                    'title': str, 
                    'questions_count': int,
                    'created_at': str (дата)
                }]
        """
        base_text = (
            "📋 <b>Выберите опрос для планирования</b>\n\n"
            "ℹ️ <i>Инструкция:</i>\n"
            "1. Просмотрите список ваших опросов ниже\n"
            "2. Нажмите на кнопку с нужным опросом\n"
            "3. Система перейдет к выбору пациента\n\n"
            "🔍 <b>Доступные опросы:</b>"
        )
        
        if not has_surveys:
            return (
                f"{base_text}\n\n"
                "😔 <i>У вас нет доступных опросов</i>\n\n"
                "✏️ Создайте новый опрос через меню"
            )
            
        return base_text
    
    @staticmethod
    def get_survey_planning_template(survey_dbm: SurveyDBM) -> str:
        """Бланк выбранного опроса для планирования прохождения пациентом
        
        Args:
            survey: Объект опроса SurveyDBM
        """
        status_emoji = "🟢" if survey_dbm.is_active else "🔴"
        status_text = "Активен" if survey_dbm.is_active else "Неактивен"
        
        base_text = (
            "📋 <b>Подтверждение выбора опроса</b>\n\n"
            f"<b>Название:</b> {survey_dbm.title}\n"
            f"<b>ID опроса:</b> {survey_dbm.id}\n"
            f"<b>Статус:</b> {status_emoji} {status_text}\n"
        )
        
        if survey_dbm.description:
            base_text += f"\n<b>Описание:</b>\n{survey_dbm.description}\n"
        
        base_text += (
            "\nℹ️ <i>Что дальше?</i>\n"
            "1. <b>Подтвердите</b> выбор этого опроса кнопкой ниже\n"
            "2. После подтверждения вы перейдете к выбору пациента\n"
            "🔍 <b>Проверьте информацию об опросе выше</b>\n"
            "👇 <b>Подтвердите выбор или измените решение</b>"
        )
        
        return base_text
    
    @staticmethod
    def get_patient_selection_template(
        survey_dbm: SurveyDBM, 
        user_id: int,
        has_patients: bool = True,
    ) -> str:
        """Бланк выбора пациента после подтверждения опроса
        
        Args:
            survey_dbm: Объект опроса
            has_patients: Есть ли прикрепленные пациенты
            user_id: ID врача в системе (для подстановки в инструкцию)
        """
        base_text = (
            "👤 <b>Выбор пациента для опроса</b>\n\n"
            f"📋 <b>Опрос:</b> {survey_dbm.title} (ID: {survey_dbm.id})\n\n"
        )
        
        if not has_patients:
            instruction = (
                "ℹ️ <i>У вас пока нет прикрепленных пациентов</i>\n\n"
                "📌 <b>Как пациенту закрепиться за вами:</b>\n"
                "1. Пациент должен открыть меню в боте\n"
                "2. Выбрать 'Закрепиться за доктором'\n"
                "3. Найти вас и нажать подтвердить\n"
                f"4. Либо ввести ваш ID: <code>{user_id}</code>\n\n"
            )
                
            instruction += "После этого пациент появится в вашем списке"
            return f"{base_text}{instruction}"
        
        return (
            f"{base_text}"
            "ℹ️ <i>Инструкция:</i>\n"
            "1. Выберите пациента из списка ниже\n"
            "2. Подтвердите выбор пациента\n"
            "3. Укажите дату и время прохождения\n\n"
            "👇 <b>Используйте кнопки ниже для выбора</b>"
        )
    
    @staticmethod
    def get_patient_confirmation_template(
        survey_dbm: SurveyDBM,
        patient_dbm: UserDBM,
        doctor_id: int
    ) -> str:
        """Бланк подтверждения выбранного пациента
        
        Args:
            survey_dbm: Объект опроса (SurveyDBM)
            patient_dbm: Объект пациента (UserDBM)
            doctor_id: ID врача в системе
        """
        return (
            "✅ <b>Подтверждение выбора пациента</b>\n\n"
            f"📋 <b>Опрос:</b> {survey_dbm.title} (ID: {survey_dbm.id})\n"
            f"👤 <b>Пациент:</b> {patient_dbm.full_name}\n"
            f"🆔 <b>Telegram ID:</b> <code>{patient_dbm.tg_id}</code>\n"
            f"👨⚕️ <b>Ваш ID:</b> <code>{doctor_id}</code>\n\n"
            "ℹ️ <i>Проверьте данные пациента перед подтверждением</i>\n\n"
            "👇 <b>Подтвердите выбор или измените решение</b>"
        )
    
    @staticmethod
    def get_multiple_times_confirmation_blank(survey: Survey) -> str:
        """Специфичный бланк для подтверждения нескольких опросов в день"""
        times = "\n".join(
            f"• {(datetime.combine(datetime.today(), t) + timedelta(hours=5)).time().strftime('%H:%M')}" 
            for t in survey.schedule_times
        )
        return (
            "🔄 <b>Тип опроса: опрос несколько раз в день</b>\n\n"
            f"📋 <b>Название опроса:</b> {survey.survey_dbm.title}\n"
            f"👤 <b>Пациент:</b> {survey.patient_dbm.full_name}\n\n"
            f"🔢 <b>Количество прохождений в день:</b> {survey.times_per_day}\n"
            f"⏰ <b>Установленное время для прохождений:</b>\n{times}\n\n"
            f"📅 <b>Период:</b> {survey.start_date.strftime('%d.%m.%Y')} - {survey.end_date.strftime('%d.%m.%Y')}\n\n"
            "🔔 <b>Напоминания:</b>\n"
            f"• Будут приходить если опрос не пройден\n"
            f"• Максимум {survey.max_reminders} напоминания в день\n\n"
            "👇 <b>Подтвердите или измените параметры</b>"
        )
    
    @staticmethod
    def get_once_per_day_confirmation_blank(survey: Survey) -> str:
        """Специфичный бланк для подтверждения ежедневного опроса"""
        times = "\n".join(
            f"• {(datetime.combine(datetime.today(), t) + timedelta(hours=5)).time().strftime('%H:%M')}" 
            for t in survey.schedule_times
        )
        return (
            "☀️ <b>Тип опроса: ежедневный опрос</b>\n\n"
            f"📋 <b>Название опроса:</b> {survey.survey_dbm.title}\n"
            f"👤 <b>Пациент:</b> {survey.patient_dbm.full_name}\n\n"
            f"⏰ <b>Установленное время для прохождения:</b> {times}\n"
            f"📅 <b>Период:</b> {survey.start_date.strftime('%d.%m.%Y')} - {survey.end_date.strftime('%d.%m.%Y')}\n\n"
            "🔔 <b>Напоминания:</b>\n"
            f"• Будут приходить если опрос не пройден\n"
            f"• Максимум {survey.max_reminders} напоминания в день\n\n"
            "👇 <b>Подтвердите или измените параметры</b>"
        )

    @staticmethod
    def get_every_few_days_confirmation_blank(survey: Survey) -> str:
        """Специфичный бланк для подтверждения опроса раз в несколько дней"""
        times = "\n".join(
            f"• {(datetime.combine(datetime.today(), t) + timedelta(hours=5)).time().strftime('%H:%M')}" 
            for t in survey.schedule_times
        )
        day_form = "день" if survey.interval_days == 1 else "дня" if 2 <= survey.interval_days <= 4 else "дней"
        return (
            "📆 <b>Тип опроса: опрос раз в несколько дней</b>\n\n"
            f"📋 <b>Название опроса:</b> {survey.survey_dbm.title}\n"
            f"👤 <b>Пациент:</b> {survey.patient_dbm.full_name}\n\n"
            f"🔄 <b>Интервал:</b> Каждые {survey.interval_days} {day_form}\n"
            f"⏰ <b>Установленное время для прохождения:</b> {times}\n"
            f"📅 <b>Период:</b> {survey.start_date.strftime('%d.%m.%Y')} - {survey.end_date.strftime('%d.%m.%Y')}\n\n"
            "🔔 <b>Напоминания:</b>\n"
            f"• Будут приходить если опрос не пройден\n"
            f"• Максимум {survey.max_reminders} напоминания в день\n\n"
            "👇 <b>Подтвердите или измените параметры</b>"
        )

    @staticmethod
    def get_survey_planning_confirmation_blank(survey: Survey) -> str:
        if survey.frequency_type is ScheduledSurveyDBM.FrequencyType.MULTIPLE_TIMES_PER_DAY:
            return DoctorBlank.get_multiple_times_confirmation_blank(survey)
        elif survey.frequency_type is ScheduledSurveyDBM.FrequencyType.ONCE_PER_DAY:
            return DoctorBlank.get_once_per_day_confirmation_blank(survey)
        else:
            return DoctorBlank.get_every_few_days_confirmation_blank(survey)