from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

admin_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="👨‍💻 Найти пользователя", callback_data='admin_search_user')
        ],
        [
            InlineKeyboardButton(text="📨 Рассылка", callback_data='admin_newsletter_first'),
            InlineKeyboardButton(text="📊 Статистика", callback_data='admin_statistics')
        ]
    ]
)

admin_cancel_action = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="❌ Отменить", callback_data='admin_cancel_action')
        ]
    ]
)

admin_back_to_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="↩️ Вернуться", callback_data='admin_cancel_action')
        ]
    ]
)


def admin_find_user(user_id: int, status_ban: int, is_admin: bool) -> InlineKeyboardMarkup:
    admin_find_user_kb = []
    if not is_admin:
        if status_ban == 0:
            admin_find_user_kb.append(
                [InlineKeyboardButton(text="🩸 Забанить", callback_data=f'admin_ban_user_{user_id}')])
        elif status_ban == 1:
            admin_find_user_kb.append(
                [InlineKeyboardButton(text="🦠 Разбанить", callback_data=f'admin_unban_user_{user_id}')])

    admin_find_user_kb.append(
        [InlineKeyboardButton(text="↩️ Вернуться", callback_data='admin_cancel_action')])

    admin_find_user_kb = InlineKeyboardMarkup(inline_keyboard=admin_find_user_kb)
    return admin_find_user_kb
