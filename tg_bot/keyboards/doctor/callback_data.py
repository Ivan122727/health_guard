from enum import Enum

class DoctorAction(str, Enum):
    CHANGE_FULL_NAME = "change_full_name"
    CREATE_TITLE_SURVEY = "create_title_survey"
    EDIT_SURVEY_TITLE = "edit_survey_title"
    CONFIRM_TITLE_SURVEY = "confirm_title_survey"
    CHOOSE_TYPE_QUESTION = "choose_type_question"
    CREATE_TEMPLATE_QUESTION = "create_template_question"
    CONFIRM_CREATE_TEMPLATE_QUESTION = "confirm_create_template_question"
    CREATE_NEW_QUESTION = "create_new_question"
    CONFIRM_CREATE_NEW_QUESTION = "confirm_create_new_question"
    
    # Управление опросом
    SAVE_SURVEY = "save_survey"
    EDIT_SURVEY = "edit_survey"
    CANCEL_CREATE_SURVEY = "cancel_create_survey"
    
    # Редактирование опроса
    EDIT_QUESTION = "edit_question"
    SET_CURRENT_QUESTION = "set_current_question"
    REMOVE_CURRENT_QUESTION = "remove_current_question"
    FINISH_EDITING = "finish_editing"

    SCHEDULE_SURVEY = "schedule_survey"
    GET_LIST_QUESTIONS = "list_questions"