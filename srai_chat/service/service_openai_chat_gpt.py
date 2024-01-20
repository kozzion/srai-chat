from typing import Optional, Tuple

from openai import OpenAI

from srai_chat.dao.dao_prompt_config import PromptConfig
from srai_chat.service.context_manager import ContextManager
from srai_chat.service.service_base import ServiceBase


class ServiceOpenaiChatGpt(ServiceBase):
    def __init__(self, context_manager: ContextManager, openai_api_key: str):
        super().__init__(context_manager)
        if openai_api_key is None:
            raise Exception("api_key_open_ai not set")

        # Create a new client and connect to the server
        self.client_openai = OpenAI(api_key=openai_api_key)

    def get_default_model_id(self) -> str:
        return "gpt-3.5-turbo"

    def list_model_id(self) -> list:
        model_list = self.client_openai.models.list().data
        return [model.id for model in model_list]

    def prompt_default(self, user_message_content: str, *, model: Optional[str] = None) -> str:
        if model is None:
            model = self.get_default_model_id()
        prompt_config_input = PromptConfig.create(model, "You are a helpfull assistent")
        prompt_config_input = prompt_config_input.append_user_message(user_message_content)
        prompt_config_result = self.prompt_for_prompt_config(prompt_config_input)
        return prompt_config_result.list_message[-1]["content"]

    def prompt_for_prompt_config(self, prompt_config_input: PromptConfig) -> PromptConfig:
        completion = self.client_openai.chat.completions.create(
            model=prompt_config_input.model,
            messages=prompt_config_input.list_message,  # type: ignore
        )
        return prompt_config_input.append_assistent_message(completion.choices[0].message.content)  # type: ignore

    def prompt_for_prompt_config_cached(self, prompt_config_input: PromptConfig) -> Tuple[PromptConfig, bool]:
        from srai_chat.service.context_manager import ContextManager

        dao = ContextManager().get_instance().service_persistency.dao_prompt_config
        prompt_config_result = dao.load_prompt_config_cached(prompt_config_input)
        if prompt_config_result is not None:
            return prompt_config_result, True

        else:
            prompt_config_result = self.prompt_for_prompt_config(prompt_config_input)
            dao.save_prompt_config_cached(prompt_config_input, prompt_config_result)
            return prompt_config_result, False
