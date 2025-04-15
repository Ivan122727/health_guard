from enum import Enum
from typing import Any, List, Optional, Set
import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates, Session
from sqlalchemy import event

from shared.sqlalchemy_db_.sqlalchemy_model.common import SimpleDBM
from shared.sqlalchemy_db_.sqlalchemy_model.user import UserDBM


class QuestionDBM(SimpleDBM):
    __tablename__ = "question"

    class QuestionType(str, Enum):
        """Типы вопросов."""
        TEXT = "text"
        CHOICE = "choice"
        SCALE = "scale"

        @classmethod
        def to_set(cls) -> Set[str]:
            """Возвращает множество допустимых значений типов вопросов."""
            return {role.value for role in cls}

    # Основные поля
    created_by: Mapped[int | None] = mapped_column(
        sqlalchemy.BIGINT,
        sqlalchemy.ForeignKey("user.id", ondelete="SET NULL"),
        nullable=True,
        comment="ID автора вопроса"
    )
    
    question_text: Mapped[str] = mapped_column(
        sqlalchemy.TEXT,
        nullable=False,
        comment="Текст вопроса"
    )
    
    question_type: Mapped[str] = mapped_column(
        sqlalchemy.String(20),
        nullable=False,
        comment="Тип вопроса: 'text', 'choice', 'scale'"
    )
    
    answer_options: Mapped[List[str] | None] = mapped_column(
        sqlalchemy.ARRAY(sqlalchemy.TEXT),
        nullable=True,
        comment="Варианты ответов (для типа 'choice')"
    )
    
    is_public: Mapped[bool] = mapped_column(
        sqlalchemy.BOOLEAN,
        nullable=False,
        default=False,
        comment="Доступен ли вопрос другим врачам"
    )

    # Связи
    author: Mapped[Optional[UserDBM]] = relationship(
        "UserDBM",
        foreign_keys=[created_by],
        back_populates="created_questions"
    )

    surveys: Mapped[List["SurveyQuestionDBM"]] = relationship(
        "SurveyQuestionDBM",
        back_populates="question",
        cascade="all, delete-orphan"
    )

    responses: Mapped[list["SurveyResponseDBM"]] = relationship(
        "SurveyResponseDBM",
        back_populates="question",
        cascade="all, delete-orphan"
    )

    @validates("question_type")
    def _validate_question_type(self, key: str, value: str, *args: Any, **kwargs: Any) -> str:
        """
        Валидация типа вопроса.
        
        Args:
            key: Название поля
            value: Значение для валидации
            *args: Дополнительные позиционные аргументы
            **kwargs: Дополнительные именованные аргументы
            
        Returns:
            str: Валидный тип вопроса
            
        Raises:
            ValueError: Если тип вопроса невалидный
        """
        if value not in self.QuestionType.to_set():
            raise ValueError(
                f"Тип вопроса должен быть одним из: {self.QuestionType.to_set()}. "
                f"Получено: {value}"
            )
        return value

    # TODO: Добавить валидацию для типа 'choice'
    @validates("answer_options")
    def _validate_answer_options(self, key: str, value: List[str] | None, *args: Any, **kwargs: Any) -> List[str] | None:
        """
        Валидация вариантов ответов.
        
        Args:
            key: Название поля
            value: Значение для валидации
            *args: Дополнительные позиционные аргументы
            **kwargs: Дополнительные именованные аргументы
            
        Returns:
            List[str] | None: Валидные варианты ответов
            
        Raises:
            ValueError: Если отсутствуют опции для типа 'choice'
        """
        if self.question_type == self.QuestionType.CHOICE and not value:
            raise ValueError(
                "Для вопроса типа 'choice' необходимо указать варианты ответов"
            )
        return value

    def __repr__(self) -> str:
        """Строковое представление вопроса."""
        return (
            f"{self.__class__.__name__}("
            f"id={self.id}, "
            f"question_text={self.question_text[:50]}..., "
            f"question_type={self.question_type}, "
            f"created_by={self.created_by}"
            ")"
        ) 