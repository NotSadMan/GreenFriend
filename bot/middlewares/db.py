from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from bot.db.models import User
from bot.services.repository import Repo


class DBMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        session: AsyncSession
        # Подключение к базе данных
        async with self.session_pool() as session:
            data['repo'] = Repo(session)

            statement = select(User.ban).where(User.user_id == data['event_from_user'].id)
            ban = await session.scalar(statement)
            if ban:
                return

            return await handler(event, data)
