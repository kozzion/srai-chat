import os

from srai_chat.skill.mode_chat_gpt import ModeChatGpt
from srai_chat.skill.skill_image_tag import SkillImageTag
from srai_chat.skill.skill_mode_tools import SkillModeTools


def initialize_default() -> "ContextManager":
    context = ContextManager()
    ContextManager._instance = context
    telegram_token = os.environ["TELEGRAM_TOKEN"]
    telegram_root_id = int(os.environ["TELEGRAM_ROOT_ID"])
    openai_api_key = os.environ["OPENAI_API_KEY"]
    connection_string = os.environ["MONGODB_CONNECTION_STRING"]
    database_name = os.environ["MONGODB_DATABASE_NAME"]
    from srai_chat.service.service_chat_telegram import ServiceChatTelegram
    from srai_chat.service.service_openai_chat_gpt import ServiceOpenaiChatGpt
    from srai_chat.service.service_persistency_mongo import ServicePersistencyMongo
    from srai_chat.service.service_sceduling import ServiceSceduling
    from srai_chat.service.service_skill import ServiceSkill

    context.service_chat = ServiceChatTelegram(context, telegram_token, telegram_root_id)
    context.service_persistency = ServicePersistencyMongo(context, connection_string, database_name)
    context.service_openai_chat_gpt = ServiceOpenaiChatGpt(context, openai_api_key)
    context.service_sceduling = ServiceSceduling(context)
    context.service_skill = ServiceSkill(context)

    return context


if __name__ == "__main__":
    from srai_chat.service.context_manager import ContextManager

    context_manager = initialize_default()
    # initialize services
    # ServiceSceduling.initialize(bot)
    context_manager.initialize()
    context_manager.service_chat.register_skill(SkillImageTag())
    context_manager.service_chat.register_skill(SkillModeTools())
    context_manager.service_chat.register_mode(ModeChatGpt())
    context_manager.service_chat.mode_default = context_manager.service_chat.dict_mode["ModeChatGpt"]

    # start services
    context_manager.start()  # TODO there is a race condition here
