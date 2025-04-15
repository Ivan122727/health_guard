from datetime import datetime
from typing import Optional, Union, Dict, List
import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from shared.sqlalchemy_db_.sqlalchemy_model.common import SimpleDBM
from shared.sqlalchemy_db_.sqlalchemy_model.user import UserDBM
from shared.sqlalchemy_db_.sqlalchemy_model.question import QuestionDBM
from shared.sqlalchemy_db_.sqlalchemy_model.scheduled_survey import ScheduledSurveyDBM


class SurveyResponseDBM(SimpleDBM):
    __tablename__ = "survey_responses"

    scheduled_survey_id: Mapped[Optional[int]] = mapped_column(
        sqlalchemy.BIGINT,
        sqlalchemy.ForeignKey("scheduled_surveys.id", ondelete="SET NULL"),
        nullable=True,
        comment="ID запланированного опроса"
    )
    
    patient_id: Mapped[int] = mapped_column(
        sqlalchemy.BIGINT,
        sqlalchemy.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID пациента"
    )
    
    question_id: Mapped[int] = mapped_column(
        sqlalchemy.BIGINT,
        sqlalchemy.ForeignKey("question.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID вопроса"
    )
    
    answer: Mapped[Union[str, Dict, List, None]] = mapped_column(
        sqlalchemy.TEXT,
        nullable=True,
        comment="Ответ пользователя"
    )
    
    # Связи
    scheduled_survey: Mapped[Optional["ScheduledSurveyDBM"]] = relationship(
        "ScheduledSurveyDBM",
        back_populates="responses"
    )
    
    patient: Mapped["UserDBM"] = relationship(
        "UserDBM",
        foreign_keys=[patient_id],
        back_populates="survey_responses"
    )
    
    question: Mapped["QuestionDBM"] = relationship(
        "QuestionDBM",
        back_populates="responses"
    )

    def __repr__(self) -> str:
        return (
            f"SurveyResponseDBM(id={self.id}, "
            f"patient_id={self.patient_id}, "
            f"question_id={self.question_id}, "
            f"answered_at={self.answered_at})"
        )