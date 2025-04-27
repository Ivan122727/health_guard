from datetime import date, datetime, time
from enum import Enum
from typing import List, Optional

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared.sqlalchemy_db_.sqlalchemy_model.common import SimpleDBM
from shared.sqlalchemy_db_.sqlalchemy_model.user import UserDBM
from shared.sqlalchemy_db_.sqlalchemy_model.survey import SurveyDBM


class ScheduledSurveyDBM(SimpleDBM):
    __tablename__ = "scheduled_surveys"

    class FrequencyType(str, Enum):
        MULTIPLE_TIMES_PER_DAY = "multiple_times_per_day" 
        ONCE_PER_DAY = "once_per_day"
        EVERY_FEW_DAYS = "every_few_days"

        @classmethod
        def to_set(cls) -> set[str]:
            return {item.value for item in cls}

    survey_id: Mapped[int] = mapped_column(
        sqlalchemy.BIGINT,
        sqlalchemy.ForeignKey("surveys.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID опроса"
    )
    
    patient_id: Mapped[int] = mapped_column(
        sqlalchemy.BIGINT,
        sqlalchemy.ForeignKey("user.tg_id", ondelete="CASCADE"),
        nullable=False,
        comment="ID пациента"
    )
    
    doctor_id: Mapped[Optional[int]] = mapped_column(
        sqlalchemy.BIGINT,
        sqlalchemy.ForeignKey("user.tg_id", ondelete="SET NULL"),
        nullable=True,
        comment="ID доктора"
    )
    
    frequency_type: Mapped[str] = mapped_column(
        sqlalchemy.String(50),
        nullable=False,
        comment="Тип опроса: multiple_times_per_day, once_per_day, every_few_days"
    )
    
    times_per_day: Mapped[Optional[int]] = mapped_column(
        sqlalchemy.INTEGER,
        nullable=True,
        comment="Количество опросов в день если тип (multiple_times_per_day)"
    )
    
    interval_days: Mapped[Optional[int]] = mapped_column(
        sqlalchemy.INTEGER,
        nullable=True,
        comment="Интервал в днях между опросами для типа (every_few_days)"
    )

    start_date: Mapped[date] = mapped_column(
        sqlalchemy.DATE,
        nullable=False,
        comment="Дата начала опросов"
    )
    
    end_date: Mapped[Optional[date]] = mapped_column(
        sqlalchemy.DATE,
        nullable=True,
        comment="Дата окончания опросов"
    )
    
    scheduled_times: Mapped[List[time]] = mapped_column(
        sqlalchemy.ARRAY(sqlalchemy.TIME),
        nullable=True,
        comment="Список во-сколько проходить опрос"
    )

    max_reminders: Mapped[int] = mapped_column(
        sqlalchemy.INTEGER,
        nullable=False,
        default=3,
        comment="Максимальное количество напоминаний"
    )
    
    reminder_interval_hours: Mapped[int] = mapped_column(
        sqlalchemy.INTEGER,
        nullable=False,
        default=2,
        comment="Интервал между напоминаниями (в часах)"
    )
    
    is_active: Mapped[bool] = mapped_column(
        sqlalchemy.BOOLEAN,
        nullable=False,
        default=True,
        comment="Активно ли расписание"
    )
    
    next_scheduled_date: Mapped[Optional[date]] = mapped_column(
        sqlalchemy.DATE,
        nullable=True,
        comment="Следующее запланированное время опроса"
    )

    # Связи
    survey: Mapped["SurveyDBM"] = relationship(
        "SurveyDBM",
        back_populates="scheduled_surveys"
    )
    
    patient: Mapped["UserDBM"] = relationship(
        "UserDBM",
        foreign_keys=[patient_id],
        back_populates="scheduled_surveys_as_patient"
    )
    
    doctor: Mapped[Optional["UserDBM"]] = relationship(
        "UserDBM",
        foreign_keys=[doctor_id],
        back_populates="scheduled_surveys_as_doctor"
    )

    # В ScheduledSurveyDBM добавить:
    reminders: Mapped[list["SurveyReminderDBM"]] = relationship(
        "SurveyReminderDBM",
        back_populates="scheduled_survey",
        cascade="all, delete-orphan"
    )

    responses: Mapped[list["SurveyResponseDBM"]] = relationship(
        "SurveyResponseDBM",
        back_populates="scheduled_survey",
        cascade="all, delete-orphan"
    )