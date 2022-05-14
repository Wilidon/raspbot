import datetime

from aiogram import types

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
    try:
        group_name = message.text.split(" ", 1)[1]
    except IndexError:
        await message.answer("Введите название группы: /group б-ПИНЖ-11")
        return
    resp = await sstuapi.get_groups()
    if resp.get(group_name) is None:
        await message.answer("Группа не найдена")
        return
    chat = crud.get_chat_by_chat_id(chat_id=message.chat.id)
    if chat is None:
        chat = crud.create_chat(Chat(chat_id=message.chat.id,
                                     group_id=resp.get(group_name),
                                     group_name=group_name,
                                     countdown=15))
    else:
        chat = crud.update_chat_by_chat_id(chat_id=message.chat.id,
                                           group_id=resp.get(group_name),
                                           group_name=group_name)
    await message.answer(f"Для этого чата установление "
                         f"расписание группы {group_name}.")


@dp.message_handler(commands=['rasp'])
async def main(message: types.Message):
    chat = crud.get_chat_by_chat_id(message.chat.id)
    if chat is None:
        await message.answer("Сначала установите группу "
                             "командой /group б-ПИНЖ-11")
    resp = await sstuapi.get_group(chat.group_id)
    date = datetime.date.today()
    c_day, c_month = date.day, date.month
    for k, v in resp.items():
        day, month = map(int, k.split("."))
        if c_day == day and c_month == month:
            break
    text = f"📆 Сегодня: {v['name']}\n\n"
    for lesson in v['lessons']:
        if len(lesson['lesson_teacher']) == 2:
            text += f"📚 {lesson['lesson_hour']} - " \
                    f"{lesson['lesson_room']} - " \
                    f"{lesson['lesson_type']} - " \
                    f"{lesson['lesson_teacher'][0]}\n" \
                    f"{lesson['lesson_teacher'][1]}\n"
            continue
        text += f"📚 {lesson['lesson_hour']} - " \
                f"{lesson['lesson_room']} - " \
                f"{lesson['lesson_type']} - " \
                f"{lesson['lesson_name']}\n"
    await message.answer(text)


@dp.message_handler(content_types=["text"])
async def start(message: types.Message):
    await message.answer("ok")
