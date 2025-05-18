from enum import Enum

class PatientAction(str, Enum):
    """Действия пациента"""
    CHANGE_FULL_NAME = "change_full_name"
    CONNECT_TO_DOCTOR = "connect_to_doctor"
    SELECT_DOCTOR = "select_doctor"
    CONFIRM_SELECTED_DOCTOR = "confirm_selected_doctor"
    CANCEL_CONNECT_TO_DOCTOR = "cancel_connect_to_doctor"
    START_SURVEY = "start_survey"
    ANSWER_QUESTION = "answer_question"