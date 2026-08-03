from aiogram.fsm.state import State, StatesGroup


class StatesManager(StatesGroup):
    waiting_for_config = State()
    wait_query_get_response_ai = State()
