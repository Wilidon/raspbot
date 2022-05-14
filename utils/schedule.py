import asyncio
import datetime

import pytz
from aiogram import Bot

from config import get_settings
from sql import crud
from utils import sstuapi


async def today_rasp(rasp):
    date = datetime.date.today()
    c_day, c_month = date.day, date.month
    for k, v in rasp.items():
        day, month = map(int, k.split("."))
        if c_day == day and c_month == month:
            break
    return v


async def convert_hour_to_minute(hours, minutes):
    return hours * 60 + minutes


async def scheduler():
    settings = get_settings()
    bot = Bot(token=settings.token, parse_mode="HTML")
    skip = False
    while True:
        chats = crud.get_all_chats()
        for i in chats:
            resp = await sstuapi.get_group(i.group_id)
            current_rasp = await today_rasp(resp)
            today = datetime.datetime.now(pytz.timezone('Etc/GMT-4'))
            for lesson in current_rasp['lessons']:
                hour, minute = map(int, lesson['lesson_hour'].split(":"))
                if 0 < await convert_hour_to_minute(hours=hour,
                                                    minutes=minute) - \
                        await convert_hour_to_minute(hours=today.hour,
                                                     minutes=today.minute) \
                        < i.countdown:
                    text = f"📚 Следующая пара {lesson['lesson_room']} {lesson['lesson_name']}"
                    await bot.send_message(chat_id=i.chat_id, text=text)
                    skip = True
        if skip:
            await asyncio.sleep(1000)
            skip = False
