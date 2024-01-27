from abc import ABC, abstractmethod
from typing import List

from srai_chat.command_base import CommandBase


class ChatContext:
    def __init__(
        self, chat_context_name: str, system_message_content: str, list_connected_context_name: List[str]
    ) -> None:
        self.chat_context_name = chat_context_name
        self.system_message_content = system_message_content
        self.list_connected_context_name = list_connected_context_name


class ModeState:
    def __init__(self, mode_name: str, chat_id: str, context_name: str) -> None:
        self.mode_name = mode_name
        self.chat_id = chat_id
        self.context_name = context_name


class ModeBase(ABC):
    def __init__(
        self,
    ) -> None:
        from srai_chat.service.context_manager import ContextManager  # avoiding circular import

        self.context: ContextManager = ContextManager.get_instance()
        self.mode_name = self.__class__.__name__

        self.service_chat = self.context.service_chat
        self.command_dict = {}
        self.command_context = {}

    def register_command(self, command: CommandBase):
        if command.command_name in self.command_dict:
            raise Exception(f"Command {command.command_name} already registered")
        self.command_dict[command.command_name] = command

    def register_context(self, context: ChatContext):
        if context.chat_context_name in self.command_context:
            raise Exception(f"Context {context.chat_context_name} already registered")
        self.command_context[context.chat_context_name] = context

    @abstractmethod
    def reset(
        self,
        chat_id: str,
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    def process_message(
        self,
        chat_id: str,
        message_text: str,
    ) -> None:
        raise NotImplementedError()

    # def add_command(self, command: CommandBase) -> None:
    #     self.command_dict[command.command_name] = command

    # def get_command_dict(self) -> dict:
    #     return copy(self.command_dict)

    # def has_command_audio(self) -> bool:
    #     return False

    # def get_command_audio(self) -> Callable:
    #     raise NotImplementedError()
