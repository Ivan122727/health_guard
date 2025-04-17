from shared.sqlalchemy_db_.sqlalchemy_model import UserDBM
from tg_bot.blanks import CommonBlank
from tg_bot.blanks import PatientBlank
from tg_bot.blanks import DoctorBlank


class BlankFactory:
    @staticmethod
    def get(role: str) -> type[CommonBlank]:
        keyboards = {
            UserDBM.Roles.patient: PatientBlank,
            UserDBM.Roles.doctor: DoctorBlank,
        }
        return keyboards.get(role, PatientBlank)