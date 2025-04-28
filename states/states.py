from aiogram.fsm.state import State, StatesGroup

class ProfileStates(StatesGroup):
    name = State()
    age = State()
    gender = State()
    city = State()
    bio = State()
    photo = State()
