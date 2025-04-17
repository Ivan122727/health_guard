from shared.sqlalchemy_db_.sqlalchemy_model import UserDBM
from tg_bot.keyboards import CommonKeyboard
from tg_bot.keyboards import PatientKeyboard
from tg_bot.keyboards import DoctorKeyboard


class KeyboardFactory:
    @staticmethod
    def get(role: str) -> type[CommonKeyboard]:
        keyboards = {
            UserDBM.Roles.patient: PatientKeyboard,
            UserDBM.Roles.doctor: DoctorKeyboard,
        }
        return keyboards.get(role, PatientKeyboard)