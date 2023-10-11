from aiogram.dispatcher.filters.state import StatesGroup, State

class UserRegister(StatesGroup):
    fullName = State()