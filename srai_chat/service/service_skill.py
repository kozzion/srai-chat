from ast import List
from typing import Dict

from srai_chat.command_base import CommandBase
from srai_chat.service.context_manager import ContextManager
from srai_chat.service.service_base import ServiceBase
from srai_chat.skill_base import SkillBase


class ServiceSkill(ServiceBase):
    def __init__(self, context: ContextManager) -> None:
        super().__init__(context)
        self.skill_dict: Dict[str, SkillBase] = {}
        self.command_dict: Dict[str, CommandBase] = {}

    def initialize(self) -> None:
        pass

    def register_skill(self, skill: SkillBase) -> None:
        if skill.skill_name in self.skill_dict:
            raise Exception(f"Skill {skill.skill_name} already registered")
        self.skill_dict[skill.skill_name] = skill
        for command in skill.command_dict.values():
            self.register_command(command)

    def register_command(self, command: CommandBase) -> None:
        if command.command_name in self.command_dict:
            raise Exception(f"Command {command.command_name} already registered")
        self.command_dict[command.command_name] = command

    def call_command(self, command_name: str, chat_id: str, argument_dict: dict) -> dict:
        if command_name not in self.command_dict:
            raise Exception(f"Command {command_name} not registered")
        command = self.command_dict[command_name]
        return command.execute_command(chat_id, command_name)  # TODO add command
