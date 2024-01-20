from srai_chat.dao.dao_prompt_config import PromptConfig
from srai_chat.mode_base import ModeBase


class ModeChatGpt(ModeBase):
    def __init__(self) -> None:
        super().__init__()

    def reset(
        self,
        chat_id: str,
    ) -> PromptConfig:
        from srai_chat.service.context_manager import ContextManager

        service_persistency = ContextManager.get_instance().service_persistency
        dao = service_persistency.dao_prompt_config

        promt_config_input = PromptConfig.create("gpt-4", "You are a helpfull assistent")
        dao.save_prompt_config(chat_id, promt_config_input)
        return promt_config_input

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

        service_persistency = ContextManager.get_instance().service_persistency
        service_openai_chat_gpt = ContextManager.get_instance().service_openai_chat_gpt
        dao = service_persistency.dao_prompt_config

        promt_config_input = dao.load_prompt_config(chat_id)
        if promt_config_input is None:
            promt_config_input = self.reset(chat_id)
        promt_config_input = promt_config_input.append_user_message(message_text)
        promt_config_result = service_openai_chat_gpt.prompt_for_prompt_config(promt_config_input)
        dao.save_prompt_config(chat_id, promt_config_result)
        assistent_message_content = promt_config_result.list_message[-1]["content"]
        self.service_chat.message_chat(chat_id, assistent_message_content)
