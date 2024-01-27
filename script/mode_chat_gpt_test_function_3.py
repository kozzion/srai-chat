from srai_chat.service.context_manager import ContextManager
from srai_chat.skill.mode_chat_gpt import ModeChatGpt
from srai_chat.skill.skill_image_tag import CommandImageTag
from srai_chat.skill.skill_mode_tools import CommandModeReset


def main():
    context = ContextManager.initialize_test_chat()
    context.service_skill.register_command(CommandImageTag())
    context.service_skill.register_command(CommandModeReset())

    context.service_persistency.dao_prompt_config.delete_all()
    mode = ModeChatGpt()
    context.service_chat.mode_default = mode
    mode.process_message("0", "please tell me what version of image tag the bot is running")
    mode.process_message("0", "What do you think about that?")
    while True:
        user_message_content = input()
        mode.process_message("0", user_message_content)


if __name__ == "__main__":
    main()
