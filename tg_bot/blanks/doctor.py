from tg_bot.blanks import CommonBlank


class DoctorBlank(CommonBlank):
    @staticmethod
    def get_default_blank() -> str:
        """Реализация главного меню для доктора"""
        return "Доктор"