from tg_bot.blanks import CommonBlank


class PatientBlank(CommonBlank):
    @staticmethod
    def get_default_blank() -> str:
        """Реализация главного меню для доктора"""
        return "Пациент"