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