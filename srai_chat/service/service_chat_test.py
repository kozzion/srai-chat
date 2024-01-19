from typing import List

from srai_chat.dao.dao_chat_message import ChatMessage, DaoChatMessage
from srai_chat.service.service_chat_telegram import ServiceChatTelegram


class DaoMessageTest(DaoChatMessage):
    def __init__(self):
        self.dict_message = {}

    def save_message(self, message: ChatMessage) -> None:
        self.dict_message[message.message_id] = message.to_dict()

    def load_messages(self, query: dict) -> List[dict]:
        return list(self.dict_message.values())

    def load_messages_all(self) -> List[dict]:
        return list(self.dict_message.values())


class ServiceChatTest(ServiceChatTelegram):
    def __init__(self):
        super().__init__("", 0)

    def message_chat(self, chat_id: int, text: str):
        print(text)
