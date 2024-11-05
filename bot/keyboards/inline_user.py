from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


cancel = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="❌ Отмена", callback_data='cancel')]])


async def my_plants(plants) -> InlineKeyboardMarkup:
    my_plants_kb = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text=plant.plant_name, callback_data=f'plant:{plant.plant_id}')] for plant in plants
    ])
    return my_plants_kb

async def plant_menu(plant_id, status) -> InlineKeyboardMarkup:
    status = '✅' if status else '❌'
    plant_menu_kb = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text=f"Уведомления {status}", callback_data=f'notifications:{plant_id}'),
            InlineKeyboardButton(text="Удалить", callback_data=f'delete_plant:{plant_id}')]
    ])
    return plant_menu_kb
