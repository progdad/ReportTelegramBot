from aiogram.dispatcher.filters.state import StatesGroup, State


class FSMuserbot(StatesGroup):
    start_or_back = State()

    api_id = State()
    api_hash = State()
    phone_number = State()
    password = State()
    auth_code = State()
