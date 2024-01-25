import json

from srai_chat.dao.dao_prompt_config import PromptConfig
from srai_chat.service.context_manager import ContextManager
from srai_chat.skill.skill_image_tag import CommandImageTag

context = ContextManager.initialize_test_chat()
service_openai_chat_gpt = context.service_openai_chat_gpt

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

# test toold calls
prompt_config_input = PromptConfig.create(
    service_openai_chat_gpt.get_default_model_id(),
    "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous.",
)
prompt_config_input = prompt_config_input.append_user_message("What image tag is the bot running?")
prompt_config_input = prompt_config_input.add_tool(CommandImageTag())
context.service_skill.register_command(CommandImageTag())
for tool in prompt_config_input.list_tool:
    json.dumps(tool, indent=4)


response = service_openai_chat_gpt.prompt_for_prompt_config(prompt_config_input)
print(response.list_message[-1]["content"])
