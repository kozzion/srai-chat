from abc import ABC, abstractmethod
from typing import List, Optional

from telegram import Update
from telegram.ext import CallbackContext

from srai_chat.dao.dao_chat_message import ChatMessage


class Parameter:
    def __init__(
        self,
        parameter_name: str,
        description: str,
        parameter_type: str,
        is_required: bool,
        list_enum: Optional[List[str]] = None,
    ) -> None:
        if parameter_name is None:
            raise Exception("parameter_name is None")
        if description is None:
            raise Exception("description is None")
        if parameter_type is None:
            raise Exception("parameter_type is None")
        if is_required is None:
            raise Exception("is_required is None")
        if parameter_type not in ["string", "enum"]:
            raise Exception(f"parameter_type {parameter_type} is not supported")

        if parameter_type == "enum":
            if list_enum is None:
                raise Exception("parameter_type' is 'enum' but 'list_enum' is None")
            if len(list_enum) == 0:
                raise Exception("'parameter_type' is enum but 'list_enum' is '[]'")
            dict_enum = set()
            for enum_value in list_enum:
                if enum_value is None:
                    raise Exception("enum value in 'list_enum' is None")
                if enum_value in dict_enum:
                    raise Exception(f"enum value {enum_value} is duplicate")
                dict_enum.add(enum_value)

        self.parameter_name = parameter_name
        self.description = description
        self.parameter_type = parameter_type
        self.is_required = is_required
        self.list_enum = list_enum

        from srai_chat.service.context_manager import ContextManager  # avoiding circular import

        self.context: ContextManager = ContextManager.get_instance()

    def get_gpt_description(self) -> dict:
        gpt_description = {
            "type": self.parameter_type,
            "description": self.description,
        }
        if self.parameter_type == "enum":
            gpt_description["enum"] = self.list_enum  # type: ignore
        return gpt_description


class CommandBase(ABC):
    def __init__(self, command_name: str, description: str) -> None:
        self.command_name = command_name
        self.description = description
        from srai_chat.service.context_manager import ContextManager

        self.context = ContextManager.get_instance()
        self.list_parameter: List[Parameter] = []

    def add_parameter(self, parameter: Parameter) -> None:
        for p in self.list_parameter:
            if p.parameter_name == parameter.parameter_name:
                raise Exception(f"parameter_name {parameter.parameter_name} already exists")
        self.list_parameter.append(parameter)

    def get_gpt_tool(self) -> dict:
        properties = {}
        required = []
        for parameter in self.list_parameter:
            properties[parameter.parameter_name] = parameter.get_gpt_description()
            if parameter.is_required:
                required.append(parameter.parameter_name)

        gpt_description = {
            "type": "function",
            "function": {
                "name": self.command_name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                },
            },
        }
        return gpt_description

    def execute_command_callback(self, update: Update, context: CallbackContext) -> None:
        message_id = str(update.message.message_id)
        chat_id = str(update.message.chat_id)
        author_id = str(update.message.from_user.id)
        author_name = update.message.from_user.username
        message_content = {"message_content_type": "text", "text": update.message.text}
        message = ChatMessage(message_id, chat_id, author_id, author_name, message_content)

        self.context.service_persistency.dao_message.save_message(message)

        self.execute_command(str(update.message.chat_id), update.message.text)

    @abstractmethod
    def execute_command(self, chat_id: str, command_message: str) -> dict:
        raise NotImplementedError()
