from aiogram import types, Router, F
from bot.services.repository import Repo
import bot.keyboards.inline_user as inl_kb
import bot.keyboards.reply_user as repl_kb
from bot.services.scheduler import toggle_notifications

router = Router()


async def my_plants(message: types.Message, repo: Repo):
    plants = await repo.get_plants(message.from_user.id)
    if not plants:
        await message.answer("У вас нет растений", reply_markup=repl_kb.user_menu)
        return
    await message.answer("Ваши растения:", reply_markup=await inl_kb.my_plants(plants))


async def plant_info(callback: types.CallbackQuery, repo: Repo):
    await callback.answer()
    plant_id = int(callback.data.split(':')[1])
    plant = await repo.get_plant(plant_id)
    await callback.message.answer_photo(photo=plant.plant_photo, caption=f"<b>Растение: {plant.plant_name}</b>"
                                                             f"\n\nПолив: раз в {plant.watering_frequency} дней"
                                                             f"\nПоследнее полив: {plant.last_watered.strftime('%d.%m.%Y')}",
                                        reply_markup=await inl_kb.plant_menu(plant_id, plant.notifications_enabled))

async def notifications(callback: types.CallbackQuery, repo: Repo):
    await callback.answer()
    plant_id = int(callback.data.split(':')[1])
    plant = await repo.get_plant(plant_id)
    status = not plant.notifications_enabled
    await repo.change_notifications(plant_id, status)
    await toggle_notifications(callback.from_user.id, plant_id, status, callback)
    await callback.message.answer(f"<b>Растение: {plant.plant_name}</b>"
                                  f"\n\nПолив: раз в {plant.watering_frequency} дней"
                                  f"\nПоследнее полив: {plant.last_watered.strftime('%d.%m.%Y')}",
                                  reply_markup=await inl_kb.plant_menu(plant_id, status))


async def plant_delete(callback: types.CallbackQuery, repo: Repo):
    await callback.answer()
    plant_id = int(callback.data.split(':')[1])
    await repo.delete_plant(plant_id)
    await callback.message.answer("Растение удалено", reply_markup=await inl_kb.my_plants(await repo.get_plants(callback.from_user.id)))



def register_handlers():
    router.message.register(my_plants, F.text == 'Мои растения')
    router.callback_query.register(plant_info, F.data.startswith('plant:'))
    router.callback_query.register(notifications, F.data.startswith == 'notifications')
    router.callback_query.register(plant_delete, F.data.startswith == 'delete_plant:')