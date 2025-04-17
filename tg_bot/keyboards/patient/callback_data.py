from enum import Enum

class PatientAction(str, Enum):
    """Действия пациента"""
    CHANGE_FULL_NAME = "change_full_name"
    CONNECT_TO_DOCTOR = "connect_to_doctor"
    SELECT_DOCTOR = "select_doctor"