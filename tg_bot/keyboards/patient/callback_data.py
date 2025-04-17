from enum import Enum

class PatientAction(str, Enum):
    CHANGE_FULL_NAME = "change_full_name"
    CONNECT_TO_DOCTOR = "patient:connect_to_doctor"