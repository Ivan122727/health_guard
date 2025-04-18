from aiogram.fsm.state import StatesGroup, State

class CreateNewSurveyStates(StatesGroup):
    waiting_new_question_text = State()
    waiting_new_question_options = State()