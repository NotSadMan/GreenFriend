from aiogram.fsm.context import FSMContext
from aiogram import types, Router
import bot.keyboards.admin as kb
from aiogram import html
from aiogram import F


from bot.filters.check_admin import IsAdmin
from bot.services.repository import Repo
from bot.states.state import Admin

router = Router()


async def admin_newsletter_first_step(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text('<b>📨 Рассылка</b>\n\n'
                                 'Введите сообщение:',
                                 reply_markup=kb.admin_cancel_action)
    await state.set_state(Admin.newsletter)


async def admin_cancel_action(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(f"👋 Добро пожаловать в админ-панель, "
                                 f"<b>{html.quote(call.from_user.full_name)}</b>"
                                 f"\n\nВы имеете доступ к полному контролю над ботом, с "
                                 f"помощью данной панели можно изменять "
                                 f"любые настройки бота, а также учётные записи пользователей."
                                 f"\n\nВыберите необходимое действие:",
                                 reply_markup=kb.admin_panel)
    await state.clear()


async def admin_statistics(call: types.CallbackQuery, repo: Repo):
    users_count = await repo.get_user_count()
    await call.message.edit_text('<b>📊 Статистика</b>\n\n'
                                 f'<b>Количество пользователей: {users_count}</b>',
                                 reply_markup=kb.admin_back_to_panel)


async def admin_search_user(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text('<b>📩 Поиск пользователя</b>\n\n'
                                 'Введите ID пользователя: ',
                                 reply_markup=kb.admin_cancel_action)
    await state.set_state(Admin.find_user)


async def admin_ban_user(call: types.CallbackQuery, repo: Repo):
    user_id = call.data.split('admin_ban_user_')[1]
    await repo.change_ban_status(int(user_id), 1)
    await call.message.edit_text('<b>✅ Пользователь забанен</b>\n\n',
                                 reply_markup=kb.admin_back_to_panel)


async def admin_unban_user(call: types.CallbackQuery, repo: Repo):
    user_id = call.data.split('admin_unban_user_')[1]
    await repo.change_ban_status(int(user_id), 0)
    await call.message.edit_text('<b>✅ Пользователь разбанен</b>\n\n',
                                 reply_markup=kb.admin_back_to_panel)


def register_handlers():
    router.callback_query.register(admin_newsletter_first_step, F.data == 'admin_newsletter_first', IsAdmin())
    router.callback_query.register(admin_cancel_action, F.data == 'admin_cancel_action', IsAdmin())
    router.callback_query.register(admin_statistics, F.data == 'admin_statistics', IsAdmin())
    router.callback_query.register(admin_search_user, F.data == 'admin_search_user', IsAdmin())
    router.callback_query.register(admin_ban_user, F.data.startswith("admin_ban_user_"), IsAdmin())
    router.callback_query.register(admin_unban_user, F.data.startswith("admin_unban_user_"), IsAdmin())
