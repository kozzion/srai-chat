from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


def create():
    app = FastAPI()

    @app.get("chats/")
    async def root():
        return {"message": "Hello World"}

    @app.post("/get_message/")
    async def get_messages_since(
        chat_id: str,
        timestamp: int,
    ):
        pass

    @app.post("/send_message/")
    async def send_message_text(
        chat_id: str,
        message_text: str,
    ):
        pass
