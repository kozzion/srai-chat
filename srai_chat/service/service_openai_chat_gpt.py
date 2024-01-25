import json
from typing import List, Optional, Tuple

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

    def prompt_default(self, chat_id: str, user_message_content: str, *, model: Optional[str] = None) -> str:
        if model is None:
            model = self.get_default_model_id()
        prompt_config_input = PromptConfig.create(model, "You are a helpfull assistent")
        prompt_config_input = prompt_config_input.append_user_message(user_message_content)
        prompt_config_result = self.prompt_for_prompt_config(chat_id, prompt_config_input)
        return prompt_config_result.list_message[-1]["content"]

    def prompt_for_prompt_config_cached(
        self, chat_id: str, prompt_config_input: PromptConfig
    ) -> Tuple[PromptConfig, bool]:
        from srai_chat.service.context_manager import ContextManager

        dao = ContextManager().get_instance().service_persistency.dao_prompt_config
        prompt_config_result = dao.load_prompt_config_cached(prompt_config_input)
        if prompt_config_result is not None:
            return prompt_config_result, True

        else:
            prompt_config_result = self.prompt_for_prompt_config(chat_id, prompt_config_input)
            dao.save_prompt_config_cached(prompt_config_input, prompt_config_result)
            return prompt_config_result, False

    def prompt_for_prompt_config(self, chat_id: str, prompt_config_input: PromptConfig) -> PromptConfig:
        # print(prompt_config_input.model)
        # print(prompt_config_input.list_message)
        # print(prompt_config_input.list_tool)
        # print(f"tool_choice {prompt_config_input.tool_choice}")

        completion = self.client_openai.chat.completions.create(
            model=prompt_config_input.model,
            messages=prompt_config_input.list_message,  # type: ignore
            tools=prompt_config_input.list_tool,  # type: ignore
            tool_choice=prompt_config_input.tool_choice,  # type: ignore
        )
        # print(completion.choices[0])
        list_tool_call_result: List[dict] = []
        if completion.choices[0].message.tool_calls is not None:
            for tool_call in completion.choices[0].message.tool_calls:
                tool_call_type = tool_call.type
                if tool_call_type == "function":
                    command_name = tool_call.function.name
                    tool_call_result = self.context.service_skill.call_command(
                        command_name, chat_id, tool_call.function.arguments
                    )
                    list_tool_call_result.append(tool_call_result)
                else:
                    raise Exception(f"tool_call.type {tool_call_type} not supported")
            return prompt_config_input.append_assistent_message(
                "",  # conetent will be empty
                list_tool_call_result,
            )

        else:
            return prompt_config_input.append_assistent_message(
                completion.choices[0].message.content,  # type: ignore
                list_tool_call_result,
            )
