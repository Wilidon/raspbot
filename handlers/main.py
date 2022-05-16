import datetime

from aiogram import types

from service.rasp import set_group, get_rasp
from sql import crud
from sql.models import Chat
from utils import sstuapi
from main import dp, __version__


@dp.message_handler(commands=['start'])
async def main(message: types.Message):
    text = "Бот, отправляющий в чат за 15 минут " \
           "до начала пары номер аудитории."
    await message.answer(text)


@dp.message_handler(commands=['help'])
async def main(message: types.Message):
    text = "Команда /help. Дописать!"
    await message.answer(text)


@dp.message_handler(commands=['about'])
async def main(message: types.Message):
    text = f"version: {__version__}\n" \
           "author: @wilidon\n" \
           "github: <a href='https://github.com/wilidon'>@wilidon</a>"
    await message.answer(text, disable_web_page_preview=True)


@dp.message_handler(commands=['group'])
async def main(message: types.Message):
    await message.answer(await set_group(message))


@dp.message_handler(regexp_commands=['rasp([0-9]*)'])
async def main(message: types.Message):
    await message.answer(await get_rasp(message))


@dp.message_handler(content_types=["text"])
async def start(message: types.Message):
    await message.answer("ok")
