import os

from srai_chat.service.service_chat_telegram import ServiceChatTelegram
from srai_chat.service.service_chat_test import ServiceChatTest
from srai_chat.service.service_openai_chat_gpt import ServiceOpenaiChatGpt
from srai_chat.service.service_persistency_mongo import ServicePersistencyMongo


class ContextManager:
    _instance: "ContextManager" = None  # type: ignore

    @staticmethod
    def get_instance() -> "ContextManager":
        if ContextManager._instance is None:
            raise Exception("ContextManager not initialized")
        return ContextManager._instance

    @staticmethod
    def initialize() -> None:
        ContextManager._instance = ContextManager()

    @staticmethod
    def initialize_default() -> None:
        ContextManager._instance = ContextManager()
        telegram_token = os.environ["TELEGRAM_TOKEN"]
        telegram_root_id = int(os.environ["TELEGRAM_ROOT_ID"])
        openai_api_key = os.environ["OPENAI_API_KEY"]
        connection_string = os.environ["MONGODB_CONNECTION_STRING"]
        database_name = os.environ["MONGODB_DATABASE_NAME"]

        ContextManager._instance.service_chat = ServiceChatTelegram(telegram_token, telegram_root_id)
        ContextManager._instance.service_persistency = ServicePersistencyMongo(connection_string, database_name)
        ContextManager._instance.service_openai_chat_gpt = ServiceOpenaiChatGpt(openai_api_key)

    @staticmethod
    def initialize_test_chat() -> None:
        ContextManager._instance = ContextManager()
        openai_api_key = os.environ["OPENAI_API_KEY"]
        connection_string = os.environ["MONGODB_CONNECTION_STRING"]
        database_name = os.environ["MONGODB_DATABASE_NAME"]

        ContextManager._instance.service_chat = ServiceChatTest()
        ContextManager._instance.service_persistency = ServicePersistencyMongo(connection_string, database_name)
        ContextManager._instance.service_openai_chat_gpt = ServiceOpenaiChatGpt(openai_api_key)

    def __init__(self):
        self.service_chat: ServiceChatTelegram = None  # type: ignore
        self.service_persistency: ServicePersistencyMongo = None  # type: ignore
        self.service_openai_chat_gpt: ServiceOpenaiChatGpt = None  # type: ignore
