from typing import Optional

from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    access: Optional[int] = None
    is_disable: bool = False


class Chat(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    chat_id: int
    group_id: int
    group_name: str
    countdown: int = 15
