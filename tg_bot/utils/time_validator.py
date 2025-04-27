from datetime import time
from typing import List, Tuple, Optional

class TimeValidator:
    @staticmethod
    def validate_and_parse_times(
        text: str, 
        count: int,
        sorted: bool = True,
        
    ) -> Tuple[bool, Optional[List[time]], Optional[str]]:
        """
        Валидирует и парсит введенное время для опросов
        
        Args:
            text: Введенный текст с временами
            count: Ожидаемое количество времен
            
        Returns:
            Tuple[bool, Optional[List[time]], Optional[str]]: 
                - Флаг валидности
                - Список времени или None
                - Сообщение об ошибке или None
        """
        # Разделяем ввод по запятым или переносам строк
        time_strs = [t.strip() for t in text.replace(" ", "\n").replace('\n', ',').split(',') if t.strip()]
        
        # Проверяем количество
        if len(time_strs) != count:
            return False, None, f"Нужно ввести ровно {count} времени"
        
        times = []
        for time_str in time_strs:
            try:
                # Парсим время
                if ':' in time_str:
                    hours, minutes = map(int, time_str.split(':'))
                else:
                    # Поддержка ввода только часов (например "9" вместо "09:00")
                    hours = int(time_str)
                    minutes = 0
                
                # Проверяем диапазон часов и минут
                if not (0 <= hours <= 23 and 0 <= minutes <= 59):
                    return False, None, "Часы должны быть от 0 до 23, минуты от 0 до 59"
                
                t = time(hour=hours - 5, minute=minutes)
                # Проверяем что время в допустимом диапазоне 07:00-22:00
                if t < time(2, 0) or t > time(17, 0):
                    return False, None, f"Время {t.strftime('%H:%M')} должно быть между 07:00 и 22:00"
                
                times.append(t)
                
            except ValueError:
                return False, None, f"Некорректный формат времени: {time_str}"
        
        # Проверяем временные ограничения для первого и последнего времени
        if times[0] < time(2, 0):
            return False, None, "Первый опрос не может быть раньше 07:00"
        
        if times[-1] > time(17, 0):
            return False, None, "Последний опрос не может быть позже 22:00"
        
        # Проверяем интервалы и порядок
        prev_time = None
        for t in times:
            if prev_time is not None:
                if sorted and t <= prev_time:
                    return False, None, "Времена должны быть в порядке возрастания"
                
                # Проверяем минимальный интервал 2 часа
                delta = (t.hour - prev_time.hour) * 60 + (t.minute - prev_time.minute)
                if sorted and delta < 120:
                    return False, None, "Минимальный интервал между опросами - 2 часа"
            
            prev_time = t
        
        return True, times, None