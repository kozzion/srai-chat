from srai_chat.dao.dao_prompt_config import PromptConfig
from srai_chat.mode_base import ChatContext, ModeBase
from srai_chat.skill.skill_image_tag import CommandImageTag
from srai_chat.skill.skill_mode_tools import CommandModeHistory, CommandModeReset


class ModeChatGptContext(ModeBase):
    def __init__(self) -> None:
        super().__init__()
        self.register_command(CommandImageTag())
        self.register_command(CommandModeReset())
        self.register_command(CommandModeHistory())
        self.register_context(ChatContext("base_context", "You are a helpfull assistent", ["image_tag"]))

    def reset(
        self,
        chat_id: str,
    ) -> PromptConfig:
        if chat_id is None:
            raise Exception("chat_id is None")
        from srai_chat.service.context_manager import ContextManager

        context = ContextManager.get_instance()
        service_persistency = context.service_persistency
        dao = service_persistency.dao_prompt_config

        prompt_config_input = PromptConfig.create("gpt-4", "You are a helpfull assistent")
        dao.save_prompt_config(chat_id, prompt_config_input)
        context.service_chat.message_chat(chat_id, f"Reset chat history for {chat_id}")
        return prompt_config_input

    def process_message(
        self,
        chat_id: str,
        message_text: str,
    ) -> None:
        if chat_id is None:
            raise Exception("chat_id is None")
        if message_text is None:
            raise Exception("message_text is None")
        from srai_chat.service.context_manager import ContextManager

        context = ContextManager.get_instance()
        service_persistency = context.service_persistency

        dao = service_persistency.dao_prompt_config

        prompt_config_input = dao.load_prompt_config(chat_id)

        if prompt_config_input is None:
            prompt_config_input = self.reset(chat_id)

        prompt_config_result = context.service_openai_chat_gpt.prompt_for_prompt_config(chat_id, prompt_config_input)

        dao.save_prompt_config(chat_id, prompt_config_result)
        assistent_message_content = prompt_config_result.list_message[-1]["content"]
        self.service_chat.message_chat(chat_id, assistent_message_content)
