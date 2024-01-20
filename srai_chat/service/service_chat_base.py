from abc import abstractmethod
from typing import Dict

from srai_chat.command_base import CommandBase
from srai_chat.dao.dao_chat_message import ChatMessage
from srai_chat.mode_base import ModeBase
from srai_chat.service.context_manager import ContextManager
from srai_chat.service.service_base import ServiceBase
from srai_chat.skill_base import SkillBase


class ServiceChatBase(ServiceBase):
    def __init__(self, context: ContextManager, root_id_str: str):
        super().__init__(context)
        self.root_id_str = root_id_str
        self.list_admin_id_str = [root_id_str]
        self.dict_skill: Dict[str, SkillBase] = {}
        self.dict_command: Dict[str, CommandBase] = {}
        self.mode_default: ModeBase = None  # type: ignore
        self.dict_mode: Dict[str, ModeBase] = {}
        self.dict_mode_active: Dict[str, ModeBase] = {}

    def register_mode(self, mode: ModeBase):
        if mode.mode_name in self.dict_mode:
            raise Exception(f"Mode name {mode.mode_name} already registered")
        self.dict_mode[mode.mode_name] = mode

    def register_skill(self, skill: SkillBase):
        if skill.skill_name in self.dict_skill:
            raise Exception(f"Skill name {skill.skill_name} already registered")
        self.dict_skill[skill.skill_name] = skill
        for command in skill.get_command_dict().values():
            self.register_command(command)

    def register_command(self, command: CommandBase):
        if command.command_name in self.dict_command:
            raise Exception(f"Command name {command.command_name} already registered")
        self.dict_command[command.command_name] = command
        # self.updater.dispatcher.add_handler(CommandHandler(command.command_name, command.execute_command_callback))

    def handle_text(self, message_id: str, chat_id: str, author_id: str, author_name: str, message_text: str):
        if chat_id is None:
            raise Exception("chat_id is None")

        if chat_id not in self.dict_mode_active:
            self.dict_mode_active[chat_id] = self.mode_default
        self.dict_mode_active[chat_id].process_message(chat_id, message_text)
        message_content = {"message_content_type": "text", "text": message_text}
        chat_message = ChatMessage(message_id, chat_id, author_id, author_name, message_content)
        self.context.service_persistency.dao_message.save_message(chat_message)

        # TODO move this to a skill or mode

    def message_root(self, text: str):
        self.message_chat(self.root_id_str, text=text)

    def message_admins(self, text: str):
        for admin_id in self.list_admin_id_str:
            self.message_chat(admin_id, text=text)

    @abstractmethod
    def message_chat(self, chat_id: str, text: str):
        raise NotImplementedError()
