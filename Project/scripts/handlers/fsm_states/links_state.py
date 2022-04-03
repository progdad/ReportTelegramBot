from aiogram.dispatcher.filters.state import StatesGroup, State


class FSMlinks(StatesGroup):
    links = State()
