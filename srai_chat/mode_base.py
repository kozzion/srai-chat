from abc import ABC, abstractmethod

from srai_chat.command_base import CommandBase


class ModeBase(ABC):
    def __init__(
        self,
    ) -> None:
        self.mode_name = self.__class__.__name__

        from srai_chat.service.context_manager import ContextManager  # avoiding circular import

        self.service_chat = ContextManager.get_instance().service_chat
        self.command_dict = {}

    def register_command(self, command: CommandBase):
        if command.command_name in self.command_dict:
            raise Exception(f"Command {command.command_name} already registered")
        self.command_dict[command.command_name] = command

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
