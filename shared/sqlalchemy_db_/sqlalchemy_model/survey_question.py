from typing import Any
import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from shared.sqlalchemy_db_.sqlalchemy_model.common import SimpleDBM


class SurveyQuestionDBM(SimpleDBM):
    """Модель для связи между опросами и вопросами."""
    
    __tablename__ = "survey_questions"

    survey_id: Mapped[int] = mapped_column(
        sqlalchemy.BIGINT,
        sqlalchemy.ForeignKey("surveys.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID опроса"
    )
    
    question_id: Mapped[int] = mapped_column(
        sqlalchemy.BIGINT,
        sqlalchemy.ForeignKey("question.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID вопроса"
    )
    
    order_index: Mapped[int] = mapped_column(
        sqlalchemy.INTEGER,
        nullable=False,
        comment="Порядок вопроса в опросе"
    )

    # Связи
    survey: Mapped["SurveyDBM"] = relationship(
        "SurveyDBM",
        back_populates="questions",
        foreign_keys=[survey_id]
    )
    
    question: Mapped["QuestionDBM"] = relationship(
        "QuestionDBM",
        back_populates="surveys",
        foreign_keys=[question_id]
    )

    @validates("order_index")
    def _validate_order_index(self, key: str, value: int, *args: Any, **kwargs: Any) -> int:
        """
        Валидация индекса порядка.
        
        Args:
            key: Название поля
            value: Значение для валидации
            *args: Дополнительные позиционные аргументы
            **kwargs: Дополнительные именованные аргументы
            
        Returns:
            int: Валидный индекс порядка
            
        Raises:
            ValueError: Если индекс отрицательный
        """
        if value < 0:
            raise ValueError("Индекс порядка не может быть отрицательным")
        return value

    def __repr__(self) -> str:
        """Строковое представление связи опроса и вопроса."""
        return (
            f"{self.__class__.__name__}("
            f"id={self.id}, "
            f"survey_id={self.survey_id}, "
            f"question_id={self.question_id}, "
            f"order_index={self.order_index}"
            ")"
        ) 