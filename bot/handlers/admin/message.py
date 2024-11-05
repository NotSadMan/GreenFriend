import asyncio
import contextlib
import datetime as dt
import json

from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import bot.keyboards.admin as kb
from aiogram import html

from bot.filters.check_admin import IsAdmin
from bot.services.repository import Repo
from bot.states.state import Admin

router = Router()


async def admin_message(message: types.Message):
    await message.answer(f"👋 Добро пожаловать в админ-панель, <b>{html.quote(message.from_user.full_name)}!</b>"
                         f"\n\nВы имеете доступ к полному контролю над ботом, с помощью данной панели можно изменять "
                         f"любые настройки бота, а также учётные записи пользователей."
                         f"\n\nВыберите необходимое действие:",
                         reply_markup=kb.admin_panel)


async def admin_newsletter_second_step(message: types.Message, state: FSMContext, repo: Repo):
    users = await repo.get_users()

    message_to_reply = await message.answer(
        f'<b>📨 Рассылка начата ({len(users)} пользователей)</b>'
        f'\n\nПримерное время ожидания - '
        f'{f"{len(users) * 0.1} секунд" if len(users) * 0.1 < 60 else f"{len(users) * 0.1 // 60} минут"}')
    time_start_newsletter = dt.datetime.now()
    counter = 0
    for user in users:
        with contextlib.suppress(Exception):
            await message.send_copy(user)
            counter += 1
            await asyncio.sleep(0.1)

    time_end_newsletter = dt.datetime.now()

    total_time = round((time_end_newsletter - time_start_newsletter).total_seconds())
    await message_to_reply.reply(
        f'<b>📊 Статистика по рассылке:</b>\n\n'
        f'<b>♻️ Доставлено: {counter} сообщений.</b>\n'
        f'<b>🔕 Не доставлено: {len(users) - counter} сообщений.</b>\n\n'
        f'<b>⏰ Затраченное время: '
        f'{f"{total_time} секунд" if total_time < 60 else f"{round(total_time / 60)} минут"}. </b>')
    await state.clear()


async def admin_user_profile(message: types.Message, state: FSMContext, repo: Repo, config):
    if not message.text.isdigit():
        await message.reply('Введите ID пользователя!\n\n'
                            'Пример: <code>5630011827</code>',
                            reply_markup=kb.admin_back_to_panel)
        await state.clear()
        return

    user = await repo.get_user(int(message.text))
    if user is None:
        await message.reply('Пользователь не найден.',
                            reply_markup=kb.admin_back_to_panel)
        await state.clear()
        return

    ban_status = "Админ" if user.user_id in json.loads(config['bot']['admin_ids']) else \
        ("Пользователь не в бане" if user.ban == 0 else "Пользователь в бане")

    await message.answer(
        f'<b>💻 Профиль пользователя</b>\n\n'
        f'<b>User ID:</b> {user.user_id}\n'
        f'<b>username:</b> {"@" + user.username if user.username is not None else "нет"}\n\n'
        f'<b>{ban_status}</b>',
        reply_markup=kb.admin_find_user(user.user_id, user.ban, user.user_id in json.loads(config['bot']['admin_ids'])))
    await state.clear()


def register_handlers():
    router.message.register(admin_message, Command('admin'), IsAdmin())
    router.message.register(admin_newsletter_second_step, Admin.newsletter, IsAdmin())
    router.message.register(admin_user_profile, Admin.find_user, IsAdmin())
