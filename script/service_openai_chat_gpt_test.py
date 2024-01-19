import os

from srai_chat.dao.dao_prompt_config import PromptConfig
from srai_chat.service.service_openai_chat_gpt import ServiceOpenaiChatGpt
from srai_chat.service.service_persistency import ServicePersistency

openai_api_key = os.environ["OPENAI_API_KEY"]
connection_string = os.environ["MONGODB_CONNECTION_STRING"]
database_name = os.environ["MONGODB_DATABASE_NAME"]
ServiceOpenaiChatGpt.initialize(openai_api_key=openai_api_key)
ServicePersistency.initialize(connection_string, database_name)
service_chat_gpt = ServiceOpenaiChatGpt.get_instance()
user_message_content = "Tell me something about yourself"
response = service_chat_gpt.prompt_default(user_message_content)
print(response)
prompt_config_input = PromptConfig.create(
    service_chat_gpt.get_default_model_id(), "You are a helpfull assistent", user_message_content
)
prompt_config_result, was_chashed = service_chat_gpt.prompt_for_prompt_config_cached(prompt_config_input)
print(prompt_config_result.list_message[-1]["content"])
print(was_chashed)
