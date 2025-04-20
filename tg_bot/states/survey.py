from aiogram.fsm.state import StatesGroup, State

class CreateSurveyStates(StatesGroup):
    waiting_new_title_survey = State()
    waiting_new_question_text = State()
    waiting_new_question_options = State()
    waiting_template_question_id = State()
    edit_survey = State()