from aiogram import types, Router, F
from aiogram.filters import CommandStart
from aiogram import html
from aiogram.fsm.context import FSMContext

from bot.services.repository import Repo
import bot.keyboards.reply_user as kb

router = Router()


async def start_message(message: types.Message, repo: Repo, state: FSMContext):
    await state.clear()
    await repo.add_user(message.from_user.id, message.from_user.username)
    await message.answer(f"Привет, <b>{html.quote(message.from_user.full_name)}</b>!", reply_markup=kb.user_menu)

async def cancel(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(f"Отменено", reply_markup=kb.user_menu)


def register_handlers():
    router.message.register(start_message, CommandStart())
    router.callback_query.register(cancel, F.data == 'cancel')
