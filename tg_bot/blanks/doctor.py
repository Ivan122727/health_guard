from typing import Optional
from tg_bot.blanks import CommonBlank
from tg_bot.handlers.doctor.survey_class import Question


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

    @staticmethod
    def get_survey_title_input_blank() -> str:
        """Сообщение с запросом названия опроса"""
        return (
            "📝 <b>Дайте название вашему опросу</b>\n\n"
            "✏️ <b>Требования к названию:</b>\n"
            "• Должно отражать суть опроса\n"
            "• Не длиннее 100 символов\n"
            "• Без специальных символов (@, #, $ и т.д.)\n\n"
            "📌 <b>Примеры хороших названий:</b>\n"
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
    def get_use_template_blank() -> str:
        """Инструкция для использования шаблона"""
        return (
            "📋 <b>Использование шаблонного вопроса</b>\n\n"
            "Введите <b>ID вопроса</b> из общего списка:\n"
            "• Можно найти в каталоге вопросов\n"
            "• Или получить у администратора\n\n"
            "🔢 Пример ввода ID:\n"
            "<code>12345</code>"
        )

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