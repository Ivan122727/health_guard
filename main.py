import asyncio
from datetime import date, datetime, time, timedelta
import pytz
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from shared.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from shared.sqlalchemy_db_.sqlalchemy_model import SurveyReminderDBM, ScheduledSurveyDBM


async def fetch_active_scheduled_surveys(session: AsyncSession) -> list[ScheduledSurveyDBM]:
    """
    Получаем активные опросы, которые нужно обработать сегодня.
    
    Возвращает список опросов, у которых:
    - текущая дата между start_date и end_date
    - next_scheduled_date равен сегодняшней дате
    - is_active=True
    """
    today = datetime.now(tz=pytz.UTC).date()
    
    result = await session.execute(
        sqlalchemy.select(ScheduledSurveyDBM)
        .where(ScheduledSurveyDBM.start_date <= today)
        .where(ScheduledSurveyDBM.end_date >= today)
        .where(ScheduledSurveyDBM.next_scheduled_date == today)
        .where(ScheduledSurveyDBM.is_active)
        .order_by(ScheduledSurveyDBM.id)
    )
    
    return result.scalars().unique().all()


async def fetch_todays_reminders_for_time(
    session: AsyncSession,
    survey: ScheduledSurveyDBM,
    scheduled_time: time
) -> list[SurveyReminderDBM]:
    """
    Получаем все напоминания для указанного опроса и времени, 
    которые были созданы сегодня.
    """
    today = datetime.now(tz=pytz.UTC).date()


    result = await session.execute(
        sqlalchemy.select(SurveyReminderDBM)
        .where(sqlalchemy.func.date(SurveyReminderDBM.creation_dt) == today)
        .where(SurveyReminderDBM.scheduled_survey_id == survey.id)
        .where(SurveyReminderDBM.scheduled_time == scheduled_time)
    )
    
    return result.scalars().unique().all()


async def calculate_next_reminder_time(
    session: AsyncSession,
    survey: ScheduledSurveyDBM,
    scheduled_time: time
) -> time:
    """
    Вычисляем время следующего напоминания на основе:
    - базового времени отправки
    - количества уже отправленных напоминаний
    - интервала между напоминаниями
    """
    reminders = await fetch_todays_reminders_for_time(session, survey, scheduled_time)
    
    # Вычисляем сколько часов нужно добавить к базовому времени
    hours_to_add = len(reminders) * survey.reminder_interval_hours
    
    # Создаем временную метку для вычислений
    dummy_datetime = datetime.combine(date.today(), scheduled_time)
    next_time = (dummy_datetime + timedelta(hours=hours_to_add)).time()
    
    return next_time


async def should_skip_reminders_for_time(
    session: AsyncSession,
    survey: ScheduledSurveyDBM,
    scheduled_time: time
) -> bool:
    """
    Проверяем, нужно ли пропускать напоминания для этого времени:
    - если пользователь уже завершил опрос (есть напоминание со статусом COMPLETED)
    - если достигнут лимит напоминаний (max_reminders)
    """
    reminders = await fetch_todays_reminders_for_time(session, survey, scheduled_time)
    
    # Пропускаем если пользователь уже завершил опрос
    if any(r.status == SurveyReminderDBM.ReminderStatus.COMPLETED for r in reminders):
        return True
    
    # Пропускаем если достигнут максимум напоминаний
    if len(reminders) >= survey.max_reminders:
        for reminder in reminders:
            reminder.status = SurveyReminderDBM.ReminderStatus.FAILED
            await session.flush()  # Сохраняем изменения
        return True
    
    return False


async def send_reminder_to_user(
    session: AsyncSession,
    survey: ScheduledSurveyDBM,
    scheduled_time: time
) -> None:
    """
    Отправляем напоминание пользователю или помечаем существующие как FAILED,
    если достигнут лимит.
    """
    now = datetime.now(tz=pytz.UTC)
    reminders = await fetch_todays_reminders_for_time(session, survey, scheduled_time)

    # Не отправляем если пользователь уже завершил опрос
    if any(r.status == SurveyReminderDBM.ReminderStatus.COMPLETED for r in reminders):
        return
    
    # Если достигнут лимит - помечаем все как FAILED
    if len(reminders) >= survey.max_reminders:
        for reminder in reminders:
            reminder.status = SurveyReminderDBM.ReminderStatus.FAILED
            await session.flush()  # Сохраняем изменения
        return
    
    # Создаем новое напоминание
    new_reminder = SurveyReminderDBM(
        scheduled_survey_id=survey.id,
        reminder_number=len(reminders) + 1,
        scheduled_time=scheduled_time,
        status=SurveyReminderDBM.ReminderStatus.SENT,
    )
    session.add(new_reminder)
    await session.flush()  # Сохраняем новое напоминание


async def update_survey_schedule(
    session: AsyncSession,
    survey: ScheduledSurveyDBM
) -> None:
    """
    Обновляем расписание опроса:
    - вычисляем следующую дату отправки
    - деактивируем опрос если он завершен
    """
    # Проверяем все ли напоминания для всех временных слотов обработаны
    checks = []
    for time_obj in survey.scheduled_times:
        checks.append(await should_skip_reminders_for_time(session, survey, time_obj))
    
    if not all(checks):
        return  # Не все напоминания отправлены
    
    # Вычисляем следующую дату в зависимости от типа периодичности
    if survey.frequency_type == ScheduledSurveyDBM.FrequencyType.EVERY_FEW_DAYS:
        date_diff = timedelta(days=survey.interval_days)
    else:  # DAILY
        date_diff = timedelta(days=1)
    
    next_date = survey.next_scheduled_date + date_diff
    
    print("wwewew")
    # Проверяем не выходит ли новая дата за end_date
    if survey.end_date < next_date:
        survey.next_scheduled_date = None
        survey.is_active = False
    else:
        survey.next_scheduled_date = next_date
    
    await session.flush()  # Сохраняем изменения


async def process_scheduled_surveys() -> None:
    """Основная функция для обработки запланированных опросов и отправки напоминаний."""

    async with get_cached_sqlalchemy_db().new_async_session() as session:
        try:
            surveys = await fetch_active_scheduled_surveys(session)
            if not surveys:
                return  # Нет опросов для обработки
            
            now = datetime.now(tz=pytz.UTC)

            for survey in surveys:
                if not survey.scheduled_times:
                    continue  # Нет временных слотов для отправки
                
                for scheduled_time in survey.scheduled_times:
                    # Пропускаем если уже обработано
                    if await should_skip_reminders_for_time(session, survey, scheduled_time):
                        continue
                    
                    # Вычисляем время следующего напоминания
                    next_reminder_time = await calculate_next_reminder_time(
                        session, survey, scheduled_time
                    )
                    
                    # Проверяем наступило ли время отправки
                    if now.time() >= next_reminder_time:
                        await send_reminder_to_user(session, survey, scheduled_time)
                        await update_survey_schedule(session, survey)


            await session.commit()
        except Exception as e:
            print(f"Ошибка при обработке опросов: {str(e)}")
            await session.rollback()  # Откатываем изменения в случае ошибки
            raise


if __name__ == "__main__":
    try:
        asyncio.run(process_scheduled_surveys())
    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")
