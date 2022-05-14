from bs4 import BeautifulSoup
from aiohttp import ClientSession, ClientTimeout

HOST = "https://rasp.sstu.ru"
TIMEOUT = ClientTimeout(total=5)


async def get_groups():
    async with ClientSession(timeout=TIMEOUT) as session:
        async with session.get(HOST, ssl=False) as resp:
            groups = {}
            resp = BeautifulSoup(await resp.read(), "lxml")
            for i in resp.find_all("div", {"class": "card"}):
                for j in i.find_all("div", {"class": "row groups"}):
                    for z in j.find_all("div", {"class": "col-auto group"}):
                        group_id = z.find("a")['href'].rsplit("/", 1)[1]
                        group_name = z.text
                        groups[group_name] = group_id
            return groups


async def get_group(group_id: int):
    async with ClientSession(timeout=TIMEOUT) as session:
        async with session.get(f"{HOST}/rasp/group/{group_id}",
                               ssl=False) as resp:
            lessons = {}
            counter = -1
            resp = BeautifulSoup(await resp.read(), "lxml")
            for i in resp.find_all("div", {"class": "day"}):
                counter += 1
                if counter == 0:
                    continue
                header = i.find("div", {"class": "day-header"}).find("div")
                if header is None:
                    continue
                week_name = header.find("span").text
                date = header.text.split(week_name[-1])[1]
                lessons[date] = {"name": week_name,
                                 "lessons": []}
                for j in i.find_all("div", {"class": "day-lesson"}):
                    try:
                        lesson_hour = j.find("div", {"class": "lesson-hour"}).text
                        lesson_hour = lesson_hour.split(" -", 1)[0]
                    except:
                        continue
                    lesson_room = j.find("div", {"class": "lesson-room"}).text
                    lesson_name = j.find("div", {"class": "lesson-name"}).text
                    lesson_type = j.find("div", {"class": "lesson-type"}).text
                    lesson_teacher = j.find_all("div",
                                            {"class": "lesson-teacher"})
                    if len(lesson_teacher) == 1:
                        lesson_teachers = [lesson_teacher[0].text]
                    else:
                        lesson_teachers = []
                        for t in range(len(lesson_teacher)):
                            teach_group = j.find_all("div",
                                                     {"class": "lesson-room lesson-room-1"})[t].text
                            teach_room = j.find_all("div",
                                                    {"class": "lesson-room mt-1"})[t].text
                            teach_name = j.find_all("div",
                                                    {"class": "lesson-teacher"})[t].text
                            lesson_teachers.append(f"{teach_group}{teach_room} {teach_name}")

                    lessons[date]['lessons'].append(
                        {"lesson_hour": lesson_hour,
                         "lesson_room": lesson_room,
                         "lesson_name": lesson_name,
                         "lesson_type": lesson_type,
                         "lesson_teacher": lesson_teachers})
            return lessons
