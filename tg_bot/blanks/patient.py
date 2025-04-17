from tg_bot.blanks import CommonBlank


class PatientBlank(CommonBlank):
    @staticmethod
    def get_default_blank(full_name: str) -> str:
        """Реализация главного меню для доктора"""
        text = (
            f"Добро пожаловать в MedSurvey Bot!\n\n"
            f"Ваше ФИО в системе:\n"
            f"{full_name}"
        )
        return text