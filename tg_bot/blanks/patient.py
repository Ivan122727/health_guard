from datetime import time
from shared.sqlalchemy_db_.sqlalchemy_model import UserDBM
from tg_bot.blanks import CommonBlank


class PatientBlank(CommonBlank):
    @staticmethod
    def get_default_blank(full_name: str) -> str:
        """Реализация главного меню для пациента"""
        text = (
            f"👋 Добро пожаловать в MedSurvey Bot!\n\n"
            f"📋 Ваше ФИО в системе:\n"
            f"👉 <b>{full_name}</b>\n\n"
            f"Чем могу помочь?"
        )
        return text

    @staticmethod
    def get_doctor_selection_blank() -> str:
        text = (
            f"👨⚕️👩⚕️ Выберите доктора, к которому вы хотите закрепиться!\n\n"
            f"👇 Доступные специалисты:"
        )
        return text

    @staticmethod
    def get_selected_doctor_confirm_blank(doctor_dbm: UserDBM) -> str:
        text = (
            f"🔍 Вы выбрали доктора:\n"
            f"👤 <b>{doctor_dbm.full_name}</b>\n\n"
            f"❓ Вы уверены, что хотите закрепиться за этим специалистом?\n\n"
            f"✅ Подтвердите ваш выбор:"
        )
        return text

    @staticmethod
    def get_success_doctor_attachment_blank(doctor_dbm: UserDBM) -> str:
        text = (
            f"🎉 Поздравляем!\n\n"
            f"Вы успешно закрепились за доктором:\n"
            f"👨⚕️ <b>{doctor_dbm.full_name}</b>\n\n"
            f"Теперь вы можете записываться на прием."
        )
        return text
        
    @staticmethod
    def get_survey_notification_blank(
        title: str,
        doctor_name: str, 
        scheduled_time: time,
        reminder_number: int,
        max_reminders: int = 3
    ) -> str:
        formatted_time = scheduled_time.strftime("%H:%M")
        
        text = (
            f"🔔 <b>Напоминание {reminder_number}/{max_reminders}</b>\n"
            f"🩺 Вам назначен опрос от врача\n\n"
            f"👨⚕️ <b>Врач:</b> {doctor_name}\n"
            f"📝 <b>Опрос:</b> {title}\n"
            f"⏰ <b>Время прохождения:</b> {formatted_time}\n\n"
        )
        
        if reminder_number < max_reminders:
            text += "Пожалуйста, не забудьте пройти опрос в указанное время."
        else:
            text += "⏳ <b>Последнее напоминание!</b> Пожалуйста, пройдите опрос как можно скорее."
        
        return text

    @staticmethod
    def get_survey_question_blank(
        survey_title: str,
        question_text: str,
        question_number: int,
        total_questions: int
    ) -> str:
        """
        Форматирует текст вопроса в опросе
        
        Args:
            survey_title: Название опроса
            question_text: Текст вопроса
            question_number: Номер текущего вопроса
            total_questions: Общее количество вопросов
        """
        text = (
            f"📝 <b>Опрос:</b> {survey_title}\n"
            f"🔢 <b>Вопрос {question_number} из {total_questions}</b>\n\n"
            f"❓ {question_text}\n\n"
            f"👇 Пожалуйста, выберите один из вариантов ответа:"
        )
        return text