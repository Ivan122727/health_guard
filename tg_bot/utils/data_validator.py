from datetime import date, datetime, timedelta
from typing import Optional, Tuple


class DateValidator:
    @staticmethod
    def validate_survey_dates(
        start_date_str: Optional[str],
        end_date_str: Optional[str]
    ) -> Tuple[bool, Optional[date], Optional[date], Optional[str]]:
        """
        Валидирует даты начала и окончания опроса (требуются обе даты)
        
        Args:
            start_date_str: Дата начала (ДД.ММ.ГГГГ) или None
            end_date_str: Дата окончания (ДД.ММ.ГГГГ) или None
            
        Returns:
            Кортеж: (is_valid, start_date, end_date, error_msg)
        """
        # Проверка что обе даты введены
        if not start_date_str or not end_date_str:
            return False, None, None, "Необходимо ввести обе даты - начало и конец периода"
            
        try:
            start_date = datetime.strptime(start_date_str, "%d.%m.%Y").date()
            end_date = datetime.strptime(end_date_str, "%d.%m.%Y").date()
            
            today = datetime.now().date()
            
            if start_date < today:
                return False, None, None, "Дата начала не может быть раньше сегодняшнего дня"
                
            if end_date <= start_date:
                return False, None, None, "Дата окончания должна быть после даты начала"
                
            if (end_date - start_date) < timedelta(days=1):
                return False, None, None, "Минимальная продолжительность - 1 день"
                
            if (end_date - start_date) > timedelta(days=365):
                return False, None, None, "Максимальная продолжительность - 1 год"
                
            return True, start_date, end_date, None
            
        except ValueError:
            return False, None, None, "Неверный формат даты. Используйте ДД.ММ.ГГГГ"