from aiogram.fsm.state import StatesGroup, State

class RegistrationStates(StatesGroup):
    age = State()
    gender = State()
    looking_for = State()
    city = State()
    name = State()
    bio = State()
    photo = State()
    confirm = State()
