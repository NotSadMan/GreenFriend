from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Добавить растение')
        ],
        [
            KeyboardButton(text='Мои растения'),
            KeyboardButton(text='Идентификация растения')
        ]
    ], resize_keyboard=True)
