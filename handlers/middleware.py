from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from sql.models import User
from sql import crud


class ThrottlingMiddleware(BaseMiddleware):
    """
    Мидльварь
    """

    def check_user(self, user_id: int,
                   username: str,
                   first_name: str,
                   last_name: str) -> User:
        current_user = User(user_id=user_id,
                            username=username,
                            first_name=first_name,
                            last_name=last_name,
                            access=0,
                            is_disable=False)
        return crud.create_user(user=current_user)

    async def on_process_message(self, message: types.Message, data: dict):
        data['user'] = self.check_user(user_id=message.from_user.id,
                                       username=message.from_user.username,
                                       first_name=message.from_user.first_name,
                                       last_name=message.from_user.last_name)
        if data['user'].access < 0:
            # TODO add reason and time end of block
            await message.answer(text="Вы забанены")
            # BaseMiddleware(False)
            raise CancelHandler()

    # async def on_process_callback_query(self, update: types.CallbackQuery, data: dict):
    #     db = get_db()
    #     db.append("inline_clicks", 1)
    #     user = self.check_user(user_id=update.from_user.id,
    #                            username=update.from_user.username,
    #                            first_name=update.from_user.first_name,
    #                            last_name=update.from_user.last_name)
    #     data['user'] = user
    #     data['sub'] = await self.check_sub(bot=update.bot,
    #                                        user_id=update.from_user.id)
    #     if user.access < 0:
    #         await update.message.edit_text(text="Вы забанены")
    #         raise CancelHandler()
