from srai_chat.dao.dao_prompt_config import PromptConfig
from srai_chat.mode_base import ModeBase


class ModeChatgpt(ModeBase):
    def __init__(self) -> None:
        super().__init__()

    def process_message(self, chat_id_str: str, user_message_content: str) -> None:
        from srai_chat.service.context_manager import ContextManager

        service_persistency = ContextManager.get_instance().service_persistency
        service_openai_chat_gpt = ContextManager.get_instance().service_openai_chat_gpt
        dao = service_persistency.dao_prompt_config

        promt_config_input = dao.load_prompt_config(chat_id_str)
        if promt_config_input is None:
            promt_config_input = PromptConfig.create("gpt-4", "You are a helpfull assistent")
        promt_config_input = promt_config_input.append_user_message(user_message_content)
        promt_config_result = service_openai_chat_gpt.prompt_for_prompt_config(promt_config_input)
        dao.save_prompt_config(chat_id_str, promt_config_result)
        assistent_message_content = promt_config_result.list_message[-1]["content"]
        self.service_chat.message_chat(int(chat_id_str), assistent_message_content)
