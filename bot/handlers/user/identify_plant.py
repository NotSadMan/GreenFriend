from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
import bot.keyboards.inline_user as inl_kb
from typing import Dict
import os
import bot.keyboards.reply_user as repl_kb
from bot.states.state import Plant
from bot.services.identify_api import identify_plant_from_image

router = Router()


async def identify_plant(message: types.Message, state: FSMContext):
    await message.answer(f"<b>Отправьте изображение растения: </b>", reply_markup=inl_kb.cancel)
    await state.set_state(Plant.photo_for_identification)


async def photo_for_identification(message: types.Message, state: FSMContext):
    await state.clear()
    if message.photo is None:
        await message.answer(f"<b>Отменено</b>")
        return
    photo_path = f"bot/photo/{message.from_user.id}.jpg"

    await message.bot.download(message.photo[0].file_id, destination=photo_path)
    try:
        plant_info = await identify_plant_from_image(photo_path)
    except Exception as e:
        await message.answer("<b>Произошла ошибка при идентификации растения.</b>")
        print(f"Ошибка при идентификации растения: {e}")
        return
    result_message = format_plant_info(plant_info)
    await message.answer(result_message, reply_markup=repl_kb.user_menu)
    os.remove(photo_path)

def format_plant_info(plant_info: Dict) -> str:
    """Форматирует информацию о растении в удобный для чтения текст."""
    result_message = (
        f"<b>Скорее всего, ваше растение — это {plant_info['species']}!</b>\n\n"
        f"<b>Научное название:</b>\n"
        f"• <b>Вид:</b> {plant_info['species']}\n"
        f"• <b>Род:</b> {plant_info['genus']}\n"
        f"• <b>Семейство:</b> {plant_info['family']}\n"
        f"• <b>Автор:</b> {plant_info['author']}\n\n"
        f"<b>Общие названия:</b>\n"
        + "\n".join(f"• {name}" for name in plant_info['common_names']) + "\n\n"
        f"<b>Изображения:</b>\n"
    )
    for image_type in ['leaf', 'flower', 'habit', 'bark', 'other']:
        if plant_info['images'][image_type]:
            result_message += f"• <a href='{plant_info['images'][image_type]}'>{image_type.capitalize()}</a>\n"
    if plant_info['cabi_link']:
        result_message += f"\n<b>Полезные ссылки:</b>\n• <a href='{plant_info['cabi_link']}'>CABI</a>"
    return result_message


def register_handlers():
    router.message.register(identify_plant, F.text == 'Идентификация растения')
    router.message.register(photo_for_identification, Plant.photo_for_identification)
