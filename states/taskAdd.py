from aiogram.dispatcher.filters.state import StatesGroup, State

class TaskDataAdd(StatesGroup):
    yesterday = State()
    today = State()
    tomorrow = State()
    data_verification = State()