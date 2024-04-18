from aiogram.filters.state import StatesGroup, State

class RegisterState(StatesGroup):
    name = State()
    lastname = State()
    firstname = State()
    new_firstname = State()
    submit = State()
    new_lastname = State()