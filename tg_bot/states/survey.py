from aiogram.fsm.state import StatesGroup, State

class CreateSurveyStates(StatesGroup):
    waiting_choose_type_question = State()
    waiting_create_new_question_select = State()
    waiting_create_template_question_select = State()
    waiting_new_title_survey = State()
    waiting_new_question_text = State()
    waiting_new_question_options = State()
    waiting_template_question_id = State()
    edit_survey = State()

class ScheduleSurveyStates(StatesGroup):
    waiting_choose_type_survey = State()
    # Тип несколько раз в день
    waiting_choose_multiple_times_per_day = State()
    waiting_set_times_per_day = State()
    # Тип один раз в день
    waiting_choose_once_per_day = State()
    # Тип раз в несколько дней    
    waiting_choose_every_few_days = State()
    waiting_set_interval_days = State()
    # Ввод периода
    waiting_survey_period = State()
    waiting_select_survey = State()
    waiting_confirm_selected_survey = State()
    waiting_select_patient = State()