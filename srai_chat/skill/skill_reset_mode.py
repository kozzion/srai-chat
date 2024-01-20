import os

from srai_chat.command_base import CommandBase
from srai_chat.skill_base import SkillBase


class CommandResetMode(CommandBase):
    def __init__(self, skill: SkillBase) -> None:
        super().__init__(skill, "image_tag")

    def execute_command(self, chat_id: str, command_message: str) -> None:
        from srai_chat.service.context_manager import ContextManager

        ContextManager.get_instance().service_chat.mode_default.reset(chat_id)


class SkillResetMode(SkillBase):
    def __init__(self):
        super().__init__()
        self.add_command(CommandResetMode(self))
