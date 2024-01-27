from srai_chat.service.context_manager import ContextManager
from srai_chat.skill.mode_chat_gpt import ModeChatGpt
from srai_chat.skill.skill_image_tag import CommandImageTag
from srai_chat.skill.skill_mode_tools import CommandModeHistory, CommandModeReset

context = ContextManager.initialize_test_chat()

context.service_persistency.dao_prompt_config.delete_all()
context.service_skill.register_command(CommandImageTag())

context.service_skill.register_command(CommandModeReset())

context.service_skill.register_command(CommandModeHistory())
mode = ModeChatGpt()
context.service_chat.mode_default = mode
mode.process_message("0", "Tell me something about yourself")
while True:
    user_message_content = input()
    mode.process_message("0", user_message_content)
