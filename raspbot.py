import asyncio

from aiogram import Dispatcher, Bot
from aiogram.utils import executor
from sqlmodel import SQLModel

from config import get_settings
from handlers.middleware import ThrottlingMiddleware

__version__ = "0.1.2"

from utils.schedule import scheduler

loop = asyncio.get_event_loop()
settings = get_settings()
bot = Bot(token=settings.token, parse_mode="HTML")
dp = Dispatcher(bot=bot, loop=loop)


async def on_startup(_):
    asyncio.create_task(scheduler())
    pass

if __name__ == '__main__':
    from handlers import dp
    from sql.db import engine, SQLModel
    SQLModel.metadata.create_all(engine)

    dp.middleware.setup(ThrottlingMiddleware())
    executor.start_polling(dp, skip_updates=False)
