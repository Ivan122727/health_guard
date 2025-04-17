import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared.sqlalchemy_db_.sqlalchemy_model.common import SimpleDBM
from shared.sqlalchemy_db_.sqlalchemy_model.user import UserDBM

class DoctorPatientDBM(SimpleDBM):
    """Модель для связи многие-ко-многим между доктором и пациентом."""
    
    __tablename__ = "doctor_patient"

    doctor_id: Mapped[int] = mapped_column(
        sqlalchemy.BIGINT,
        sqlalchemy.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID доктора"
    )
    
    patient_id: Mapped[int] = mapped_column(
        sqlalchemy.BIGINT,
        sqlalchemy.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID пациента"
    )

    # Связи
    doctor: Mapped[UserDBM] = relationship(
        "UserDBM",
        foreign_keys=[doctor_id],
        back_populates="patient_relations"
    )
    
    patient: Mapped[UserDBM] = relationship(
        "UserDBM",
        foreign_keys=[patient_id],
        back_populates="doctor_relations"
    )

    # Уникальный индекс для пары доктор-пациент
    __table_args__ = (
        sqlalchemy.UniqueConstraint('doctor_id', 'patient_id', name='uq_doctor_patient'),
    )

    def __init__(self, doctor: UserDBM, patient: UserDBM, **kwargs):
        """
        Инициализация связи между доктором и пациентом.
        
        Args:
            doctor: Объект доктора
            patient: Объект пациента
            
        Raises:
            ValueError: Если роли пользователей не соответствуют ожидаемым
        """
        if doctor.role != UserDBM.Roles.doctor:
            raise ValueError(f"Пользователь с ID {doctor.id} не является доктором")
            
        if patient.role != UserDBM.Roles.patient:
            raise ValueError(f"Пользователь с ID {patient.id} не является пациентом")
            
        super().__init__(doctor=doctor, patient=patient, **kwargs)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(doctor_id={self.doctor_id}, patient_id={self.patient_id})" 