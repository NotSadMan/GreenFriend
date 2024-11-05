import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram import Bot, Dispatcher
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from bot.db.base import Base

from bot.filters.chat_type import ChatTypeFilter
from router_manager import setup_routers
from aiogram.client.default import DefaultBotProperties

from bot.middlewares.db import DBMiddleware
from config import load_config

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()



async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")
    config = load_config("bot/config/bot.ini")

    router = setup_routers()

    bot = Bot(token=config['bot']['token'], default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(config=config)
    dp.include_routers(router)

    DATABASE_URL = (f"postgresql+asyncpg://{config['db']['user']}:{config['db']['password']}@{config['db']['host']}:"
                    f"{config['db']['port']}/{config['db']['name']}")

    engine = create_async_engine(DATABASE_URL, pool_size=20, max_overflow=0)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


    # Регистрация Middlewares
    dp.update.outer_middleware(DBMiddleware(sessionmaker))

    """
    ВАЖНО. 
    Бот работает исключительно в личных сообщениях, поменяйте значение в фильтре, если необходимо изменить это.
    ChatTypeFilter(chat_type=["group", "supergroup"])
    """

    # Регистрация фильтров
    dp.message.filter(
        ChatTypeFilter(chat_type=["private"])
    )

    # start
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


def cli():
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")


if __name__ == '__main__':
    cli()
