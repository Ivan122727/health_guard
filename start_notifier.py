import asyncio
import pytz
import sqlalchemy
from aiogram import Bot
from datetime import date, datetime, time, timedelta
from aiogram.enums import ParseMode
from typing import List, Optional
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.client.default import DefaultBotProperties

from shared.config import BotSettings
from shared.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from shared.sqlalchemy_db_.sqlalchemy_model import SurveyReminderDBM, ScheduledSurveyDBM, SurveyDBM
from tg_bot.blanks.patient import PatientBlank
from tg_bot.handlers.common.message_service import MessageService
from tg_bot.keyboards.patient.patient import PatientKeyboard

class NotificationSender:
    def __init__(self, settings: BotSettings):
        self.bot = Bot(
            token=settings.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )

    async def send_notification(
        self, 
        scheduled_survey: ScheduledSurveyDBM,
        scheduled_time: time,
        reminder_number: int,
        notification_id: int,
    ) -> bool:
        """Отправить уведомление пользователю.
        
        Args:
            user_id: ID пользователя
            message: Текст сообщения
            
        Returns:
            bool: Результат отправки (True - успешно, False - ошибка)
        """
        adjusted_time = (datetime.combine(datetime.min, scheduled_time) + timedelta(hours=5)).time()

        await MessageService.send_managed_message(
            bot=self.bot,
            user_id=scheduled_survey.patient_id,
            text=PatientBlank.get_survey_notification_blank(
                title=scheduled_survey.survey.title,
                doctor_name=scheduled_survey.doctor.full_name,
                scheduled_time=adjusted_time,
                reminder_number=reminder_number,
                max_reminders=scheduled_survey.max_reminders,
            ),
            reply_markup=PatientKeyboard.get_survey_notification_keyboard(notification_id=notification_id)
        )
        print(notification_id)


class SurveyReminderProcessor:
    """Обработчик напоминаний для опросов."""
    
    def __init__(self, session: AsyncSession, notification_sender: Optional[NotificationSender] = None):
        """Инициализация процессора.
        
        Args:
            session: Асинхронная сессия SQLAlchemy
            notification_sender: Отправитель уведомлений (опционально)
        """
        self.session = session
        self.notification_sender = notification_sender
    
    async def fetch_active_scheduled_surveys(self) -> List[ScheduledSurveyDBM]:
        """Получить активные опросы для обработки сегодня.
        
        Возвращает опросы, у которых:
        - Текущая дата между start_date и end_date
        - next_scheduled_date равен сегодняшней дате
        - is_active=True
        
        Returns:
            List[ScheduledSurveyDBM]: Список активных опросов
        """
        today = datetime.now(tz=pytz.UTC).date()
        
        result = await self.session.execute(
            sqlalchemy.select(ScheduledSurveyDBM)
            .options(
                joinedload(ScheduledSurveyDBM.survey),
                joinedload(ScheduledSurveyDBM.patient),
                joinedload(ScheduledSurveyDBM.doctor)
            )
            .where(ScheduledSurveyDBM.is_active)
            .where(ScheduledSurveyDBM.start_date <= today)
            .where(ScheduledSurveyDBM.end_date >= today)
            .where(ScheduledSurveyDBM.next_scheduled_date == today)
            .order_by(ScheduledSurveyDBM.id)
        )
        
        return result.scalars().unique().all()
    
    async def fetch_todays_reminders_for_time(
        self,
        survey: ScheduledSurveyDBM,
        scheduled_time: time
    ) -> List[SurveyReminderDBM]:
        """Получить напоминания для указанного времени сегодня.
        
        Args:
            survey: Объект опроса
            scheduled_time: Время отправки
            
        Returns:
            List[SurveyReminderDBM]: Список напоминаний
        """
        today = datetime.now(tz=pytz.UTC).date()

        result = await self.session.execute(
            sqlalchemy.select(SurveyReminderDBM)
            .where(sqlalchemy.func.date(SurveyReminderDBM.creation_dt) == today)
            .where(SurveyReminderDBM.scheduled_survey_id == survey.id)
            .where(SurveyReminderDBM.scheduled_time == scheduled_time)
        )
        
        return result.scalars().unique().all()
    
    async def calculate_next_reminder_time(
        self,
        survey: ScheduledSurveyDBM,
        scheduled_time: time
    ) -> time:
        """Вычислить время следующего напоминания.
        
        Args:
            survey: Объект опроса
            scheduled_time: Базовое время отправки
            
        Returns:
            time: Время следующего напоминания
        """
        reminders = await self.fetch_todays_reminders_for_time(survey, scheduled_time)
        
        # Вычисляем сколько часов нужно добавить к базовому времени
        hours_to_add = len(reminders) * survey.reminder_interval_hours
        
        # Создаем временную метку для вычислений
        dummy_datetime = datetime.combine(date.today(), scheduled_time)
        next_time = (dummy_datetime + timedelta(hours=hours_to_add)).time()
        
        return next_time
    
    async def should_skip_reminders_for_time(
        self,
        survey: ScheduledSurveyDBM,
        scheduled_time: time
    ) -> bool:
        """Проверить, нужно ли пропускать напоминания для этого времени.
        
        Пропускаем если:
        - Пользователь уже завершил опрос (есть напоминание со статусом COMPLETED)
        - Достигнут лимит напоминаний (max_reminders)
        
        Args:
            survey: Объект опроса
            scheduled_time: Время отправки
            
        Returns:
            bool: Нужно ли пропускать
        """
        reminders = await self.fetch_todays_reminders_for_time(survey, scheduled_time)
        
        # Пропускаем если пользователь уже завершил опрос
        if any(r.status == SurveyReminderDBM.ReminderStatus.COMPLETED for r in reminders):
            return True
        
        # Пропускаем если достигнут максимум напоминаний
        if len(reminders) >= survey.max_reminders:
            # for reminder in reminders:
            #     reminder.status = SurveyReminderDBM.ReminderStatus.FAILED
            #     await self.session.flush()
            return True
        
        return False
    
    async def send_reminder_to_user(
        self,
        survey: ScheduledSurveyDBM,
        scheduled_time: time
    ) -> None:
        """Отправить напоминание пользователю.
        
        Args:
            survey: Объект опроса
            scheduled_time: Время отправки
        """
        reminders = await self.fetch_todays_reminders_for_time(survey, scheduled_time)

        # Не отправляем если пользователь уже завершил опрос
        if any(r.status == SurveyReminderDBM.ReminderStatus.COMPLETED for r in reminders):
            return
        
        # Если достигнут лимит - помечаем все как FAILED
        if len(reminders) >= survey.max_reminders:
            for reminder in reminders:
                reminder.status = SurveyReminderDBM.ReminderStatus.FAILED
                await self.session.flush()
            return
        
        # Создаем новое напоминание
        new_reminder = SurveyReminderDBM(
            scheduled_survey_id=survey.id,
            reminder_number=len(reminders) + 1,
            scheduled_time=scheduled_time,
            status=SurveyReminderDBM.ReminderStatus.SENT,
            creation_dt=datetime.now(tz=pytz.UTC),
        )

        self.session.add(new_reminder)
        await self.session.flush()
        await self.session.refresh(new_reminder)

        # Отправляем уведомление, если настроен отправитель
        if self.notification_sender:
            await self.notification_sender.send_notification(
                scheduled_survey=survey, 
                scheduled_time=scheduled_time,
                reminder_number=len(reminders) + 1,
                notification_id=new_reminder.id,
            )
    
    async def update_survey_schedule(
    self,
    survey: ScheduledSurveyDBM
    ) -> None:
        """Обновить расписание опроса.
        
        Вычисляет следующую дату отправки или деактивирует опрос.
        
        Args:
            survey: Объект опроса
        """
        # Проверяем все ли напоминания для всех временных слотов обработаны
        checks = []
        for time_obj in survey.scheduled_times:
            checks.append(await self.should_skip_reminders_for_time(survey, time_obj))
        
        if not all(checks):
            return  # Не все напоминания отправлены
        
        # Проверяем, что next_scheduled_date не None
        if survey.next_scheduled_date is None:
            survey.is_active = False
            await self.session.flush()
            return
        
        # Вычисляем следующую дату в зависимости от типа периодичности
        if survey.frequency_type == ScheduledSurveyDBM.FrequencyType.EVERY_FEW_DAYS:
            date_diff = timedelta(days=survey.interval_days)
        else:  # DAILY
            date_diff = timedelta(days=1)
        
        next_date = survey.next_scheduled_date + date_diff
        
        # Проверяем не выходит ли новая дата за end_date
        if survey.end_date < next_date:
            survey.next_scheduled_date = None
            survey.is_active = False
        else:
            survey.next_scheduled_date = next_date
        
        await self.session.flush()


class SurveyNotifier:
    """Основной класс для планирования и обработки уведомлений об опросах."""
    
    def __init__(self, interval_minutes: int = 15, notification_sender: Optional[NotificationSender] = None):
        """Инициализация планировщика.
        
        Args:
            interval_minutes: Интервал проверки в минутах (по умолчанию 15)
            notification_sender: Отправитель уведомлений (опционально)
        """
        self.interval_minutes = interval_minutes
        self.notification_sender = notification_sender
        self._is_running = False
    
    async def process_scheduled_surveys(self) -> None:
        """Обработать запланированные опросы и отправить напоминания."""
        async with get_cached_sqlalchemy_db().new_async_session() as session:
            try:
                processor = SurveyReminderProcessor(session, self.notification_sender)
                surveys = await processor.fetch_active_scheduled_surveys()
                if not surveys:
                    return  # Нет опросов для обработки
                
                now = datetime.now(tz=pytz.UTC)

                for survey in surveys:
                    if not survey.scheduled_times:
                        continue  # Нет временных слотов для отправки
                    
                    for scheduled_time in survey.scheduled_times:
                        # Пропускаем если уже обработано
                        if await processor.should_skip_reminders_for_time(survey, scheduled_time):
                            await processor.update_survey_schedule(survey)
                            continue
                        
                        # Вычисляем время следующего напоминания
                        next_reminder_time = await processor.calculate_next_reminder_time(
                            survey, scheduled_time
                        )
                        
                        # Проверяем наступило ли время отправки
                        if now.time() >= next_reminder_time:
                            await processor.send_reminder_to_user(survey, scheduled_time)
                            await processor.update_survey_schedule(survey)

                await session.commit()
            except Exception as e:
                print(f"Ошибка при обработке опросов: {str(e)}")
                await session.rollback()
                raise
    
    async def start(self) -> None:
        """Запустить планировщик с указанным интервалом."""
        self._is_running = True
        while self._is_running:
            try:
                await self.process_scheduled_surveys()
            except Exception as e:
                print(f"Ошибка в цикле планировщика: {str(e)}")

            minute = 30

            await asyncio.sleep(self.interval_minutes * minute)
    
    async def stop(self) -> None:
        """Остановить планировщик."""
        self._is_running = False


async def main():
    """Точка входа для планировщика."""
    notification_settings = BotSettings()
    notification_sender = NotificationSender(settings=notification_settings)

    notifier = SurveyNotifier(interval_minutes=1, notification_sender=notification_sender)
    try:
        await notifier.start()
    except KeyboardInterrupt:
        await notifier.stop()
    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")
        await notifier.stop()


if __name__ == "__main__":
    asyncio.run(main())