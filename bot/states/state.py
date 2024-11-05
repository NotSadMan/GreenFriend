from aiogram.fsm.state import StatesGroup, State


class Admin(StatesGroup):
    newsletter = State()
    find_user = State()
    ban = State()

class Plant(StatesGroup):
    name = State()
    photo = State()
    watering_frequency = State()
    photo_for_identification = State()

