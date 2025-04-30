from aiogram.fsm.state import State, StatesGroup

class OrderForm(StatesGroup):
    name = State()
    contact_method = State()
    telegram_confirm = State()
    contact_details = State()
    help_needed = State()
    confirm = State()