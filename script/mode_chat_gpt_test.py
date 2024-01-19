import os

from srai_chat.service.context_manager import ContextManager
from srai_chat.skill.mode_chat_gpt import ModeChatgpt

ContextManager.initialize_test_chat()

mode = ModeChatgpt()
mode.process_message("0", "Tell me something about yourself")
while True:
    user_message_content = input()
    mode.process_message("0", user_message_content)
