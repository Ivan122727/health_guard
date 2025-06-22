# health_guard

# STACK

- Python 3.12
- FastAPI, SQLAlchemy, SQLAdmin, Aiogram, Openpyxl
- Poetry (poetry-core>=2.0.0,<3.0.0)

# Run

1. Run ```./manage/create_db.sh```
2. Run ```PYTHONPATH=./ poetry run python tests/make_test_data_1.py```
3. Run ```./manage/restart_services.sh```

# Реализованный функционал

## ТГ-Бот
### Создание опросов
### Планирование прохождение опросов
### Уведомление пациентов о опросах
### Выгрузка списка доступных для добавления по ID вопросов в excel формате
### Выгрузка статистики прохождения опроса пациентами
## Админ Панель
### Редактирование ролей
### Добавление публичных вопросов
### Деактивация профиля пользователя
### Редактирование данных в БД
[Админ панель](http://87.228.96.60:5665/admin/)

[ТГ-БОТ](https://t.me/HelpMedSurveyBot)

[Видео Демонстрация](https://disk.yandex.ru/d/Fybp7e_DPfrZ4w)