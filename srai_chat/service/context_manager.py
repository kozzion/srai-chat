import os


class ContextManager:
    _instance: "ContextManager" = None  # type: ignore

    @staticmethod
    def get_instance() -> "ContextManager":
        if ContextManager._instance is None:
            raise Exception("ContextManager not initialized")
        return ContextManager._instance

    def initialize(self) -> None:
        if self.service_sceduling is not None:
            self.service_sceduling.initialize()
        if self.service_chat is not None:
            self.service_chat.initialize()

    def start(self) -> None:
        if self.service_sceduling is not None:
            self.service_sceduling.start()
        if self.service_chat is not None:
            self.service_chat.start()

    @staticmethod
    def initialize_test_chat() -> "ContextManager":
        context = ContextManager()
        ContextManager._instance = context
        openai_api_key = os.environ["OPENAI_API_KEY"]
        connection_string = os.environ["MONGODB_CONNECTION_STRING"]
        database_name = os.environ["MONGODB_DATABASE_NAME"]

        from srai_chat.service.service_chat_test import ServiceChatTest
        from srai_chat.service.service_openai_chat_gpt import ServiceOpenaiChatGpt
        from srai_chat.service.service_persistency_mongo import ServicePersistencyMongo
        from srai_chat.service.service_sceduling import ServiceSceduling
        from srai_chat.service.service_skill import ServiceSkill

        context.service_chat = ServiceChatTest(context)
        context.service_persistency = ServicePersistencyMongo(context, connection_string, database_name)
        context.service_openai_chat_gpt = ServiceOpenaiChatGpt(context, openai_api_key)
        context.service_sceduling = ServiceSceduling(context)
        context.service_skill = ServiceSkill(context)
        return context

    def __init__(self):
        from srai_chat.service.service_chat_base import ServiceChatBase
        from srai_chat.service.service_openai_chat_gpt import ServiceOpenaiChatGpt
        from srai_chat.service.service_persistency_mongo import ServicePersistencyMongo
        from srai_chat.service.service_sceduling import ServiceSceduling
        from srai_chat.service.service_skill import ServiceSkill

        self.service_chat: ServiceChatBase = None  # type: ignore
        self.service_persistency: ServicePersistencyMongo = None  # type: ignore
        self.service_openai_chat_gpt: ServiceOpenaiChatGpt = None  # type: ignore
        self.service_sceduling: ServiceSceduling = None  # type: ignore
        self.service_skill: ServiceSkill = None  # type: ignore
