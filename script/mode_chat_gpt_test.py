import os

from srai_chat.dao.dao_prompt_config import PromptConfig
from srai_chat.service.service_openai_chat_gpt import ServiceOpenaiChatGpt
from srai_chat.service.service_persistency import ServicePersistency
from srai_chat.skill.mode_chat_gpt import ModeChatgpt

openai_api_key = os.environ["OPENAI_API_KEY"]
connection_string = os.environ["MONGODB_CONNECTION_STRING"]
database_name = os.environ["MONGODB_DATABASE_NAME"]
ServiceOpenaiChatGpt.initialize(openai_api_key=openai_api_key)
ServicePersistency.initialize(connection_string, database_name)
mode = ModeChatgpt()
result = model.process_message("Tell me something about yourself")
while True:
    print(result)
    user_message_content = input()
    result = model.process_message(user_message_content)
prompt_config_input = PromptConfig.create(
    service_chat_gpt.get_default_model_id(), "You are a helpfull assistent", user_message_content
)
prompt_config_result, was_chashed = service_chat_gpt.prompt_for_prompt_config_cached(prompt_config_input)
print(prompt_config_result.list_message[-1]["content"])
print(was_chashed)
