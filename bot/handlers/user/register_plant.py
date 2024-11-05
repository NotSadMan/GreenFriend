from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from bot.services.repository import Repo
from bot.states.state import Plant
import bot.keyboards.reply_user as repl_kb
import bot.keyboards.inline_user as inl_kb

router = Router()


async def add_plant(message: types.Message, state: FSMContext):
    await message.answer(f"<b>Введите имя вашего растения: </b>", reply_markup=inl_kb.cancel)
    await state.set_state(Plant.name)


async def name_add(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(f"<b>Отправьте изображение вашего растения: </b>", reply_markup=inl_kb.cancel)
    await state.set_state(Plant.photo)


async def photo_add(message: types.Message, state: FSMContext):
    if message.photo is None:
        await message.answer(f"<b>Отправьте изображение вашего растения: </b>")
        return
    await state.update_data(photo=message.photo[0].file_id)
    await message.answer(f"<b>Укажите частоту полива в днях(если раз в неделю - то напишите цифру 7): </b>",
                         reply_markup=inl_kb.cancel)
    await state.set_state(Plant.watering_frequency)


async def watering_frequency_add(message: types.Message, repo: Repo, state: FSMContext):
    data = await state.get_data()
    await repo.add_plant(message.from_user.id, data['name'], data['photo'], int(message.text))
    await state.clear()
    await message.answer(f"<b>Растение добавлено!</b>", reply_markup=repl_kb.user_menu)


def register_handlers():
    router.message.register(add_plant, F.text == 'Добавить растение')
    router.message.register(name_add, Plant.name)
    router.message.register(photo_add, Plant.photo)
    router.message.register(watering_frequency_add, Plant.watering_frequency)
