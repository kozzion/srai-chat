import json
from hashlib import sha256
from typing import Dict, List, Optional

from srai_chat.command_base import CommandBase
from srai_chat.dao.dao_mongo_base import DaoMongoBase

# class PromptConfig:
#     def __init__(
#         self,
#         model: str,
#         role: str,
#         message_content: str,
#         list_tool_call_result: List[dict] = [],
#         list_tool: Optional[List[dict]] = None,
#         tool_choice: Optional[str] = None,
#         response_format: Optional[str] = None,
#     ):


class PromptConfig:
    def __init__(
        self,
        model: str,
        list_message: List[Dict[str, str]],
        list_list_tool_call_result: List[List[dict]] = [],
        list_tool: Optional[List[dict]] = None,
        tool_choice: Optional[str] = None,
        response_format: Optional[str] = None,
    ):
        if model is None:
            raise Exception("model is None")
        if list_message is None:
            raise Exception("list_message is None")
        if response_format is not None:
            if response_format not in ["json"]:
                raise Exception(f"response_format {response_format} not in [json]")
        if tool_choice is not None:
            if tool_choice not in ["none", "auto"]:
                raise Exception(f"tool_choice {tool_choice} not in [none, auto]")
        self.model = model
        self.list_message = list_message
        self.list_list_tool_call_result = list_list_tool_call_result
        self.list_tool = list_tool

        self.response_format = response_format
        self.tool_choice: Optional[str] = tool_choice

    def to_dict(self) -> dict:
        return {
            "model": self.model,
            "list_message": self.list_message,
            "list_list_tool_call_result": self.list_list_tool_call_result,
            "list_tool": self.list_tool,
            "response_format": self.response_format,
            "tool_choice": self.tool_choice,
        }

    def set_response_format(self, response_format: str) -> "PromptConfig":
        return PromptConfig(
            self.model,
            self.list_message,
            self.list_list_tool_call_result,
            self.list_tool,
            response_format,
            self.tool_choice,
        )

    def set_tool_choice(self, tool_choice: str) -> "PromptConfig":
        # tool_choice ="none"
        # tool_choice ="auto"
        # tool_choice={"type": "function", "function": {"name": "get_n_day_weather_forecast"}
        return PromptConfig(self.model, self.list_message, self.list_list_tool_call_result, self.list_tool, tool_choice)

    def add_tool(self, command_base: CommandBase) -> "PromptConfig":
        tool_new = command_base.get_gpt_tool()
        # TODO type tools
        if self.list_tool is not None:
            for tool in self.list_tool:
                if tool["type"] == "function":
                    if tool["function"]["name"] == tool_new["function"]["name"]:
                        raise Exception(f"tool {tool_new['function']['name']} already in list_tool")
            list_tool = self.list_tool.copy()
        else:
            list_tool = []
        # ensure no duplicate functions

        list_tool.append(tool_new)
        return PromptConfig(self.model, self.list_message, self.list_list_tool_call_result, list_tool, self.tool_choice)

    def apppend_message(
        self, role: str, message_content: str, list_tool_call_result: List[dict] = []
    ) -> "PromptConfig":
        if role not in ["system", "user", "assistant"]:
            raise Exception(f"role {role} not in [system, user, assistant]")
        list_message = self.list_message.copy()
        list_list_tool_call_result = self.list_list_tool_call_result.copy()
        list_message.append(
            {
                "role": role,
                "content": message_content,
            }
        )
        list_list_tool_call_result.append(list_tool_call_result)
        return PromptConfig(self.model, list_message, list_list_tool_call_result)

    def append_system_message(self, message_content: str) -> "PromptConfig":
        return self.apppend_message("system", message_content, [])

    def append_user_message(self, message_content: str) -> "PromptConfig":
        return self.apppend_message("user", message_content, [])

    def append_assistent_message(self, message_content: str, list_tool_call_result: List[dict] = []) -> "PromptConfig":
        return self.apppend_message("assistant", message_content, list_tool_call_result)

    @staticmethod
    def create(
        model: str,
        system_message_content: str,
    ) -> "PromptConfig":
        list_message = []
        list_message.append({"role": "system", "content": system_message_content})

        return PromptConfig(model, list_message)

    @staticmethod
    def from_dict(dict_prompt_config: dict) -> "PromptConfig":
        model = dict_prompt_config["model"]
        list_message = dict_prompt_config["list_message"]
        list_list_tool_call_result = dict_prompt_config["list_list_tool_call_result"]
        list_tool = dict_prompt_config["list_tool"]
        response_format = dict_prompt_config["response_format"]
        tool_choice = dict_prompt_config["tool_choice"]
        return PromptConfig(model, list_message, list_list_tool_call_result, list_tool, tool_choice, response_format)


class DaoPromptConfig(DaoMongoBase):
    def __init__(self, connection_string: str, database_name: str) -> None:
        super().__init__(connection_string, database_name, "prompt_config")

    def save_prompt_config_cached(self, prompt_config_input: PromptConfig, prompt_config_result: PromptConfig) -> None:
        id = sha256(json.dumps(prompt_config_input.to_dict()).encode("utf-8")).hexdigest()
        self.save_prompt_config(id, prompt_config_result)

    def save_prompt_config(self, id: str, prompt_config_result: PromptConfig) -> None:
        prompt_config_result_dict = prompt_config_result.to_dict()
        prompt_config_result_dict["_id"] = id
        self.update_one({"_id": id}, {"$set": prompt_config_result_dict}, upsert=True)

    def load_prompt_config_cached(self, prompt_config_input: PromptConfig) -> Optional[PromptConfig]:
        id = sha256(json.dumps(prompt_config_input.to_dict()).encode("utf-8")).hexdigest()
        return self.load_prompt_config(id)

    def load_prompt_config(self, id: str) -> Optional[PromptConfig]:
        query = {"_id": id}
        result = self.find(query)
        # convert curser to list
        list_result = list(result)
        if len(list_result) == 0:
            return None
        else:
            dict_prompt_config = list_result[0]
            return PromptConfig.from_dict(dict_prompt_config)

    def load_prompt_config_all(self) -> List[dict]:
        return self.find({})  # type: ignore
