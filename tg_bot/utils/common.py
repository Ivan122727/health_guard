import re
from typing import Optional


def validate_and_normalize_full_name(raw_name: str) -> str:
    """
    Валидирует и очищает введенное полное имя.
    
    Параметры:
        raw_name (str): Сырая строка с ФИО
        
    Возвращает:
        str: Нормализованное ФИО
        
    Исключения:
        ValueError: Если имя не прошло валидацию
        
    Правила валидации:
        - Минимум 2 слова (имя, фамилия и отчество)
        - Максимум 100 символов в сумме
        - Каждая часть имени от 2 до 25 символов
        - Только буквы, пробелы и дефисы
        - Без цифр и специальных символов
        - Автоматическая капитализация
    """
    # Удаление всех недопустимых символов (кроме букв, пробелов и дефисов)
    sanitized = re.sub(r"[^a-zA-Zа-яА-ЯёЁ\s-]", "", raw_name.strip())
    
    # Проверка на наличие цифр
    if any(char.isdigit() for char in sanitized):
        raise ValueError("ФИО не должно содержать цифр")
    
    # Нормализация пробелов
    sanitized = re.sub(r"\s+", " ", sanitized)
    name_parts = sanitized.split()
    
    # Валидация количества слов
    if len(name_parts) < 2:
        raise ValueError("Введите имя, фамилию и отчество (минимум 2 слова)")
    
    # Валидация каждой части имени
    for part in name_parts:
        if len(part) < 2:
            raise ValueError(f"Часть имени '{part}' слишком короткая (минимум 2 символа)")
        if len(part) > 25:
            raise ValueError(f"Часть имени '{part}' слишком длинная (максимум 25 символов)")
    
    # Валидация общей длины
    if len(sanitized) > 100:
        raise ValueError("Слишком длинное ФИО (максимум 100 символов)")
    
    # Нормализация регистра (Первая буква заглавная, остальные строчные)
    normalized = " ".join(
        part[0].upper() + part[1:].lower() if part else ""
        for part in name_parts
    )
    
    return normalized