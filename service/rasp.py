import datetime

from aiogram import types

from sql import crud
from sql.models import Chat
from utils import sstuapi


async def set_group(message: types.Message):
    try:
        group_name = message.text.split(" ", 1)[1]
    except IndexError:
        return "Введите название группы: /group б-ПИНЖ-11"
    resp = await sstuapi.get_groups()
    if resp.get(group_name) is None:
        return "Группа не найдена"

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
    return f"Для этого чата установление расписание группы {group_name}."


async def get_rasp_by_day(chat_id, study_day):
    is_today = True if study_day == 1 else False
    if study_day > 25:
        return False
    resp = await sstuapi.get_group(chat_id)
    date = datetime.date.today() + datetime.timedelta(days=study_day - 1)
    c_day, c_month = date.day, date.month
    for k, v in resp.items():
        day, month = map(int, k.split("."))
        if c_day == day and c_month == month:
            break
    text = f"📆 Сегодня: {v['name']}\n\n"
    is_study_day = False
    if is_today:
        h, m = map(int,
                   v['lessons'][len(v['lessons']) - 1]['lesson_hour'].split(
                       ":"))
        today = datetime.datetime.today()
        last_pair_time = datetime.datetime(year=today.year, month=today.month,
                                           day=today.day,
                                           hour=h + 2, minute=m)
        if today > last_pair_time:
            return await get_rasp_by_day(chat_id=chat_id,
                                         study_day=study_day + 1)
    for lesson in v['lessons']:
        is_study_day = True
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
    if is_study_day:
        text += f"\nНа следующий день: /rasp{study_day + 1}"
        return text
    return await get_rasp_by_day(chat_id=chat_id,
                                 study_day=study_day + 1)


async def get_rasp(message: types.Message):
    chat = crud.get_chat_by_chat_id(message.chat.id)
    if chat is None:
        return "Сначала установите группу командой /group б-ПИНЖ-11"
    try:
        study_day = int(message.text.split("rasp")[1])
    except:
        study_day = 1
    try:
        resp = await get_rasp_by_day(chat_id=chat.group_id,
                                     study_day=study_day)
    except:
        raise
        return "Расписание не найдено."
    if resp is False:
        return "Расписание не найдено."
    return resp
