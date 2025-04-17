from enum import Enum

class DoctorAction(str, Enum):
    CHANGE_FULL_NAME = "change_full_name"
    CREATE_SURVEY = "doctor:create_survey"
    SCHEDULE_SURVEY = "doctor:schedule_survey"
    GET_LIST_QUESTIONS = "doctor:list_questions"