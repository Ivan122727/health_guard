from enum import Enum

class DoctorAction(str, Enum):
    CHANGE_FULL_NAME = "change_full_name"
    CREATE_SURVEY = "create_survey"
    CREATE_TEMPLATE_SURVEY = "create_template_survey"
    CONFIRM_CREATE_TEMPLATE_SURVEY = "confirm_create_template_survey"
    CREATE_NEW_SURVEY = "create_new_survey"
    CONFIRM_CREATE_NEW_SURVEY = "confirm_create_new_survey"

    SCHEDULE_SURVEY = "schedule_survey"
    GET_LIST_QUESTIONS = "list_questions"