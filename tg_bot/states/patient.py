from aiogram.fsm.state import StatesGroup, State


class ConnectToDoctorStates(StatesGroup):
    waiting_select_doctor = State()
    waiting_confirm_doctor = State()