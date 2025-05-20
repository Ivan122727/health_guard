from enum import Enum

class DoctorAction(str, Enum):
    # Управление главным меню
    CHANGE_FULL_NAME = "change_full_name"
    CREATE_TITLE_SURVEY = "create_title_survey"
    SCHEDULE_SURVEY = "schedule_survey"
    GET_LIST_QUESTIONS = "list_questions"
    GET_SURVEYS_STATICS = "get_surveys_statics"

    # Создание опроса
    EDIT_SURVEY_TITLE = "edit_survey_title"
    CONFIRM_TITLE_SURVEY = "confirm_title_survey"
    CHOOSE_TYPE_QUESTION = "choose_type_question"
    CREATE_TEMPLATE_QUESTION = "create_template_question"
    CONFIRM_CREATE_TEMPLATE_QUESTION = "confirm_create_template_question"
    CREATE_NEW_QUESTION = "create_new_question"
    CONFIRM_CREATE_NEW_QUESTION = "confirm_create_new_question"
    SAVE_SURVEY = "save_survey"
    EDIT_SURVEY = "edit_survey"
    CANCEL_CREATE_SURVEY = "cancel_create_survey"
    EDIT_QUESTION = "edit_question"
    SET_CURRENT_QUESTION = "set_current_question"
    REMOVE_CURRENT_QUESTION = "remove_current_question"
    FINISH_EDITING = "finish_editing"

   # Планирование опроса
    CHOOSE_MULTIPLE_TIMES_PER_DAY = "choose_multiple_times_per_day"
    CHOOSE_ONCE_PER_DAY = "choose_once_per_day"
    CHOOSE_EVERY_FEW_DAYS = "choose_once_every_few_days"
    SET_TIMES_PER_DAY = "set_times_per_day"
    SET_INTERVAL_DAYS = "set_interval_days"
    CONFIRM_SCHEDULE = "confirm_schedule"
    CANCEL_SCHEDULING = "cancel_scheduling"
    SET_SURVEY_PERIOD = "set_survey_period"
    CONFIRM_DATE_PERIOD = "confirm_date_period"
    SELECT_SURVEY = "select_survey"
    CONFIRM_SURVEY_SELECTION = "confirm_survey_selection"
    SELECT_PATIENT = "select_patient"
    CONFIRM_SELECTED_PATIENT = "confirm_selected_patient"
    CONFIRM_SCHEDULE_SURVEY = "confirm_schedule_survey"