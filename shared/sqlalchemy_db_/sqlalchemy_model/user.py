from typing import Any, Set, List
import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship
from pydantic import validate_email
from enum import Enum

from shared.sqlalchemy_db_.sqlalchemy_model.common import SimpleDBM


class UserDBM(SimpleDBM):
    __tablename__ = "user"
 
    class Roles(str, Enum):
        doctor = "Доктор"
        patient = "Пациент"

        @classmethod
        def to_set(cls) -> Set[str]:
            """Возвращает множество допустимых значений ролей."""
            return {role.value for role in cls}

    tg_id: Mapped[str | None] = mapped_column(
        sqlalchemy.BIGINT,
        nullable=False,
        unique=True,
        comment="ID пользователя в Telegram"
    )
    
    email: Mapped[str | None] = mapped_column(
        sqlalchemy.TEXT,
        nullable=True,
        unique=True,
        comment="Email пользователя"
    )

    phone: Mapped[str | None] = mapped_column(
        sqlalchemy.TEXT,
        nullable=True,
        unique=True,
        comment="Номер телефона пользователя"
    )

    full_name: Mapped[str | None] = mapped_column(
        sqlalchemy.TEXT,
        nullable=True,
        unique=False,
        comment="ФИО пользователя"
    )

    role: Mapped[str] = mapped_column(
        sqlalchemy.TEXT,
        nullable=False,
        insert_default=Roles.patient,
        comment="Роль пользователя"
    )

    is_active: Mapped[bool] = mapped_column(
        sqlalchemy.BOOLEAN,
        nullable=False,
        insert_default=True,
        comment="Активен ли пользователь"
    )

    # Связи для докторов
    patient_relations: Mapped[List["DoctorPatient"]] = relationship(
        "DoctorPatient",
        foreign_keys="[DoctorPatient.doctor_id]",
        back_populates="doctor",
        cascade="all, delete-orphan"
    )

    # Связи для пациентов
    doctor_relations: Mapped[List["DoctorPatient"]] = relationship(
        "DoctorPatient",
        foreign_keys="[DoctorPatient.patient_id]",
        back_populates="patient",
        cascade="all, delete-orphan"
    )

    # Связь с созданными вопросами
    created_questions: Mapped[List["QuestionDBM"]] = relationship(
        "QuestionDBM",
        foreign_keys="[QuestionDBM.created_by]",
        back_populates="author",
        cascade="all, delete-orphan"
    )

    # Свойства для удобного доступа к связанным пользователям
    @property
    def patients(self) -> List["UserDBM"]:
        """Возвращает список пациентов доктора."""
        return [relation.patient for relation in self.patient_relations]

    @property
    def doctors(self) -> List["UserDBM"]:
        """Возвращает список докторов пациента."""
        return [relation.doctor for relation in self.doctor_relations]

    def __repr__(self) -> str:
        parts = [f"id={self.id}", f"tg_id={self.tg_id}", f"role={self.role}"]
        
        if self.full_name is not None:
            parts.append(f"full_name={self.full_name}")
        if self.email is not None:
            parts.append(f"email={self.email}")
        if self.phone is not None:
            parts.append(f"phone={self.phone}")
        return f"{self.entity_name} ({', '.join(parts)})"

    @validates("email")
    def _validate_email(self, key: str, value: str | None, *args: Any, **kwargs: Any) -> str | None:
        """
        Валидация email адреса.
        
        Args:
            key: Название поля
            value: Значение для валидации
            *args: Дополнительные позиционные аргументы
            **kwargs: Дополнительные именованные аргументы
            
        Returns:
            str | None: Валидный email или None
            
        Raises:
            ValueError: Если email невалидный
        """
        if value is None:
            return None
            
        if not isinstance(value, str):
            raise ValueError(f"Email должен быть строкой. Получено: {type(value)}")
            
        # Проверяем, что строка не пустая и не состоит только из пробелов
        stripped_value = value.strip()
        if not stripped_value:
            raise ValueError("Email не может быть пустым или состоять только из пробелов")
            
        try:
            validate_email(stripped_value)
            return stripped_value
        except Exception as e:
            raise ValueError(f"Ошибка валидации email {value}: {str(e)}")
    
    @validates("phone")
    def _validate_phone(self, key: str, value: str | None, *args: Any, **kwargs: Any) -> str | None:
        """
        Валидация номера телефона.
        
        Args:
            key: Название поля
            value: Значение для валидации
            *args: Дополнительные позиционные аргументы
            **kwargs: Дополнительные именованные аргументы
            
        Returns:
            str | None: Валидный номер телефона или None
            
        Raises:
            ValueError: Если номер телефона невалидный
        """
        if value is None:
            return None
            
        if not isinstance(value, str):
            raise ValueError(f"Номер телефона должен быть строкой. Получено: {type(value)}")
            
        try:
            from phonenumbers import parse, is_valid_number
            phone_number = parse(value, "RU")
            
            if not is_valid_number(phone_number):
                raise ValueError(f"Номер телефона {value} не является валидным")
                
            return value
            
        except Exception as e:
            raise ValueError(f"Ошибка валидации номера телефона {value}: {str(e)}")

    @validates("role")
    def _validate_role(self, key: str, value: str, *args: Any, **kwargs: Any) -> str:
        """
        Валидация роли пользователя.
        
        Args:
            key: Название поля
            value: Значение для валидации
            *args: Дополнительные позиционные аргументы
            **kwargs: Дополнительные именованные аргументы
            
        Returns:
            str: Валидная роль пользователя
            
        Raises:
            ValueError: Если роль невалидная
        """
        if not isinstance(value, str):
            raise ValueError(f"Роль должна быть строкой. Получено: {type(value)}")
            
        if value not in self.Roles.to_set():
            raise ValueError(f"Роль {value} не является допустимой. Допустимые роли: {self.Roles.to_set()}")
            
        return value