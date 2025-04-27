import asyncio
from datetime import date, datetime, time
import pytz
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from shared.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from shared.sqlalchemy_db_.sqlalchemy_model import SurveyReminderDBM, ScheduledSurveyDBM

# Получить опросы для которых надо уведомить пользователя
async def get_scheduled_surveys(
        session: AsyncSession
    ) -> list[ScheduledSurveyDBM]:
    now = datetime.now(tz=pytz.UTC)

    scheduled_survey_dbms = (await session.execute(
        sqlalchemy
        .select(ScheduledSurveyDBM)
        .where(ScheduledSurveyDBM.start_date <= now.date())
        .where(ScheduledSurveyDBM.end_date >= now.date())
        .where(ScheduledSurveyDBM.next_scheduled_date == now.date())
        .where(ScheduledSurveyDBM.is_active)
    )).scalars().unique().all()

    return scheduled_survey_dbms

# Получить для запланированного времени отправленные уведомления
async def get_survey_remind(
        session: AsyncSession,
        scheduled_survey_dbm: ScheduledSurveyDBM,
        scheduled_time: time
):
    now = datetime.now(tz=pytz.UTC)
    
    survey_reminder_dbms = (await session.execute(
        sqlalchemy
        .select(SurveyReminderDBM)
        .where(SurveyReminderDBM.creation_dt == now.date())
        .where(SurveyReminderDBM.scheduled_survey_id == scheduled_survey_dbm.id)
        .where(SurveyReminderDBM.scheduled_time == scheduled_time)
    )).scalars().unique().all()
    
    return survey_reminder_dbms

# Получает время во-сколько надо отправить уведомления для запланированного времени
async def get_reminder_scheduled_time(
        session: AsyncSession,
        scheduled_survey_dbm: ScheduledSurveyDBM,
        scheduled_time: time
):
    survey_reminder_dbms = await get_survey_remind(session, scheduled_survey_dbm, scheduled_time)

    return scheduled_time + time(len(survey_reminder_dbms) * scheduled_survey_dbm.reminder_interval_hours)

# Функция уведомляет пользователя если он прошел уже не уведомлеяет 
# или если кол-во уведомлений лимит привышен, статус уведомленияем меняет на FAILED
async def notify_user(
        session: AsyncSession,
        scheduled_survey_dbm: ScheduledSurveyDBM,
        scheduled_time: time
    ):
        now = datetime.now(tz=pytz.UTC)

        survey_reminder_dbms = await get_survey_remind(session, scheduled_survey_dbm, scheduled_time)

        if SurveyReminderDBM.ReminderStatus.COMPLETED in {r.status for r in survey_reminder_dbms}:
            return
        elif len(survey_reminder_dbms) == scheduled_survey_dbm.max_reminders:
            for survey_reminder_dbm in survey_reminder_dbms:
                survey_reminder_dbm.status = SurveyReminderDBM.ReminderStatus.FAILED,
                await session.refresh(survey_reminder_dbm)
        else:
            survey_reminder_dbm = SurveyReminderDBM(
                scheduled_survey_id=scheduled_survey_dbm.id,
                reminder_number=len(survey_reminder_dbms) + 1,
                scheduled_time=scheduled_time,
                status=SurveyReminderDBM.ReminderStatus.SENT,
                sent_at=now,
            )

# Функция говорит о том, что достаточно для запланированного времени на сегодня уведомлять пользователя
async def is_enogh_send_remind_for_schedule_time(
        session: AsyncSession,
        scheduled_survey_dbm: ScheduledSurveyDBM,
        scheduled_time: time
):
    now = datetime.now(tz=pytz.UTC)

    survey_reminder_dbms = await get_survey_remind(session, scheduled_survey_dbm, scheduled_time)

    if SurveyReminderDBM.ReminderStatus.COMPLETED in {r.status for r in survey_reminder_dbms}:
        return True
    elif len(survey_reminder_dbms) == scheduled_survey_dbm.max_reminders:
        return True
    
    return False

# Функция меняет для опроса в какой день нужно отправить по неме уведомления
async def update_next_schedule_date(
        session: AsyncSession,
        scheduled_survey_dbm: ScheduledSurveyDBM,
):
    # Допиши чтобы если is_enogh_send_remind_for_schedule_time для всех scheduled_survey_dbm.scheduled_times
    # То мы делаем это
    if scheduled_survey_dbm.frequency_type == ScheduledSurveyDBM.FrequencyType.EVERY_FEW_DAYS:
        diff = # Добавь scheduled_survey_dbm.interval_days дней 
    else:
        diff = # Добавь один день
    
    if # scheduled_survey_dbm.end_date < scheduled_survey_dbm.next_scheduled_date + diff:
        scheduled_survey_dbm.next_scheduled_date = None
        scheduled_survey_dbm.is_active = False
    else:
        scheduled_survey_dbm.next_scheduled_date = scheduled_survey_dbm.next_scheduled_date + diff

    await session.refresh(scheduled_survey_dbm)


async def main():
    async with get_cached_sqlalchemy_db().new_async_session() as session:
        scheduled_survey_dbms = await get_scheduled_surveys(session)

        now = datetime.now(tz=pytz.UTC)

        for scheduled_survey_dbm in scheduled_survey_dbms:
            for scheduled_time in scheduled_survey_dbm.scheduled_times:
                reminder_scheduled_time = await get_reminder_scheduled_time(
                    session,
                    scheduled_survey_dbm,
                    scheduled_time
                )

                if now.time() >= reminder_scheduled_time:
                    await notify_user(session, scheduled_survey_dbm, scheduled_time)
                    await update_next_schedule_date(session, scheduled_survey_dbm)

   
if __name__ == "__main__":
    asyncio.run(main())