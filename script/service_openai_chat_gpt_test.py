import os

from srai_chat.dao.dao_prompt_config import PromptConfig
from srai_chat.service.context_manager import ContextManager

ContextManager.initialize_test_chat()
service_openai_chat_gpt = ContextManager.get_instance().service_openai_chat_gpt

user_message_content = "Tell me something about yourself"
response = service_openai_chat_gpt.prompt_default(user_message_content)
print(response)
prompt_config_input = PromptConfig.create(
    service_openai_chat_gpt.get_default_model_id(),
    "You are a helpfull assistent",
)
prompt_config_input.append_user_message(user_message_content)
prompt_config_result, was_chashed = service_openai_chat_gpt.prompt_for_prompt_config_cached(prompt_config_input)
print(prompt_config_result.list_message[-1]["content"])
print(was_chashed)
