import json

from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject

from config import load_config


class IsAdmin(BaseFilter):

    def __init__(self):
        config = load_config("bot/config/bot.ini")
        config = config['bot']
        self.admin_ids = json.loads(config['admin_ids'])

    async def __call__(self, obj: TelegramObject) -> bool:
        return obj.from_user.id in self.admin_ids
