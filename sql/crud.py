from sqlmodel import Session, select, col

from sql.db import engine
from sql.models import User, Chat


def create_user(user: User):
    with Session(engine) as session:
        statement = select(User).where(col(User.user_id) == user.user_id)
        current_user = session.exec(statement).first()
        if current_user is None:
            session.add(user)
            session.commit()
        session.refresh(current_user)
        return current_user


def get_user_by_user_id(user_id: int):
    with Session(engine) as session:
        statement = select(User).where(col(User.user_id) == user_id)
        result = session.exec(statement)
        return result.first()


def create_chat(chat: Chat):
    with Session(engine) as session:
        statement = select(Chat).where(Chat.chat_id == chat.chat_id)
        current_chat = session.exec(statement).first()
        if current_chat is None:
            session.add(chat)
            session.commit()
        session.refresh(current_chat)
    return current_chat


def get_all_chats():
    with Session(engine) as session:
        statement = select(Chat)
        return session.exec(statement).all()


def get_chat_by_chat_id(chat_id: int):
    with Session(engine) as session:
        statement = select(Chat).where(Chat.chat_id == chat_id)
        return session.exec(statement).first()


def update_chat_by_chat_id(chat_id, group_id, group_name):
    with Session(engine) as session:
        statement = select(Chat).where(Chat.chat_id == chat_id)
        chat = session.exec(statement).first()
        chat.group_id = group_id
        chat.group_name = group_name
        session.commit()
        session.refresh(chat)
        return chat