from datetime import datetime, time
from enum import Enum
from typing import Optional

import pytz
import sqlalchemy
from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from shared.sqlalchemy_db_.sqlalchemy_model.common import SimpleDBM
from shared.sqlalchemy_db_.sqlalchemy_model.scheduled_survey import ScheduledSurveyDBM


class SurveyReminderDBM(SimpleDBM):
    __tablename__ = "survey_reminders"

    class ReminderStatus(str, Enum):
        PENDING = "pending"
        SENT = "sent"
        COMPLETED = "completed"
        FAILED = "failed"

        @classmethod
        def to_set(cls) -> set[str]:
            return {item.value for item in cls}

    scheduled_survey_id: Mapped[int] = mapped_column(
        sqlalchemy.BIGINT,
        sqlalchemy.ForeignKey("scheduled_surveys.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID запланированного опроса"
    )
    
    reminder_number: Mapped[int] = mapped_column(
        sqlalchemy.INTEGER,
        nullable=False,
        comment="Номер напоминания (1, 2, 3...)"
    )
    
    scheduled_time: Mapped[time] = mapped_column(
        sqlalchemy.TIME,
        nullable=False,
        comment="Запланированное время отправки"
    )
    
    status: Mapped[str] = mapped_column(
        sqlalchemy.String(20),
        nullable=False,
        default=ReminderStatus.PENDING,
        comment="Статус напоминания"
    )
    
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        sqlalchemy.TIMESTAMP(timezone=True),
        nullable=True,
        comment="Время завершения опроса"
    )

    # Связи
    scheduled_survey: Mapped["ScheduledSurveyDBM"] = relationship(
        "ScheduledSurveyDBM",
        back_populates="reminders"
    )

    @validates("status")
    def _validate_status(self, key: str, value: str) -> str:
        if value not in self.ReminderStatus.to_set():
            raise ValueError(
                f"Недопустимый статус напоминания. Допустимые значения: {self.ReminderStatus.to_set()}"
            )
        return value

    def __repr__(self) -> str:
        return (
            f"SurveyReminderDBM(id={self.id}, "
            f"scheduled_survey_id={self.scheduled_survey_id}, "
            f"reminder_number={self.reminder_number}, "
            f"status={self.status})"
        )