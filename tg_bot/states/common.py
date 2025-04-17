from aiogram.fsm.state import StatesGroup, State

class ChangeFullNameStates(StatesGroup):
    waiting_new_full_name = State()