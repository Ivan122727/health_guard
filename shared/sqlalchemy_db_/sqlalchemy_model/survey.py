from typing import Any, Optional, List
import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from datetime import datetime

from shared.sqlalchemy_db_.sqlalchemy_model.common import SimpleDBM
from shared.sqlalchemy_db_.sqlalchemy_model.user import UserDBM
from shared.sqlalchemy_db_.sqlalchemy_model.survey_question import SurveyQuestionDBM


class SurveyDBM(SimpleDBM):
    __tablename__ = "surveys"

    # Основные поля
    title: Mapped[str] = mapped_column(
        sqlalchemy.String(255),
        nullable=False,
        comment="Название опроса"
    )
    
    description: Mapped[str | None] = mapped_column(
        sqlalchemy.TEXT,
        nullable=True,
        comment="Описание опроса"
    )
    
    created_by: Mapped[int | None] = mapped_column(
        sqlalchemy.BIGINT,
        sqlalchemy.ForeignKey("user.tg_id", ondelete="SET NULL"),
        nullable=True,
        comment="ID создателя опроса"
    )
    
    is_active: Mapped[bool] = mapped_column(
        sqlalchemy.BOOLEAN,
        nullable=False,
        default=True,
        comment="Активен ли опрос"
    )

    # Связи
    author: Mapped[Optional[UserDBM]] = relationship(
        "UserDBM",
        foreign_keys=[created_by],
        back_populates="created_surveys"
    )

    questions: Mapped[List["SurveyQuestionDBM"]] = relationship(
        "SurveyQuestionDBM",
        back_populates="survey",
        cascade="all, delete-orphan"
    )
    # Добавить в конец класса SurveyDBM
    scheduled_surveys: Mapped[list["ScheduledSurveyDBM"]] = relationship(
        "ScheduledSurveyDBM",
        back_populates="survey",
        cascade="all, delete-orphan"
    )

    @validates("title")
    def _validate_title(self, key: str, value: str, *args: Any, **kwargs: Any) -> str:
        """
        Валидация названия опроса.
        
        Args:
            key: Название поля
            value: Значение для валидации
            *args: Дополнительные позиционные аргументы
            **kwargs: Дополнительные именованные аргументы
            
        Returns:
            str: Валидное название опроса
            
        Raises:
            ValueError: Если название пустое или слишком длинное
        """
        if not value:
            raise ValueError("Название опроса не может быть пустым")
            
        if len(value) > 255:
            raise ValueError("Название опроса не может быть длиннее 255 символов")
        
        if value.strip() == "":
            raise ValueError("Название опроса не может состоять из пробелов")

        return value

    def __repr__(self) -> str:
        """Строковое представление опроса."""
        return (
            f"{self.__class__.__name__}("
            f"id={self.id}, "
            f"title={self.title}, "
            f"created_by={self.created_by}, "
            f"is_active={self.is_active}"
            ")"
        ) 