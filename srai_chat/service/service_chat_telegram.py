from abc import ABC
from typing import Dict
from uuid import uuid4

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater

from srai_chat.command_base import CommandBase
from srai_chat.dao.dao_chat_message import ChatMessage
from srai_chat.skill_base import SkillBase


class ServiceChatTelegram(ABC):
    def __init__(
        self,
        bot_token: str,
        root_id: int,
    ):
        self.bot_token = bot_token
        self.updater: Updater = None  # type: ignore
        self.root_id = root_id
        self.list_admin_ids = [root_id]
        self.dict_skill: Dict[str, SkillBase] = {}
        self.dict_command: Dict[str, CommandBase] = {}

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
        self.updater.dispatcher.add_handler(CommandHandler(command.command_name, command.execute_command_callback))

    def handle_text(self, update: Update, context: CallbackContext):
        """Handle text messages."""
        message_id = str(update.message.message_id)
        chat_id = str(update.message.chat_id)
        author_id = str(update.message.from_user.id)
        author_name = update.message.from_user.username
        message_content = {"message_content_type": "text", "text": update.message.text}
        message = ChatMessage(message_id, chat_id, author_id, author_name, message_content)

        from srai_chat.service.context_manager import ContextManager  # TODO

        service_persistency = ContextManager.get_instance().service_persistency
        service_persistency.dao_message.save_message(message)

        # TODO move this to a skill or mode

    def message_root(self, text: str):
        self.message_chat(chat_id=self.root_id, text=text)

    def message_admins(self, text: str):
        for admin_id in self.list_admin_ids:
            self.message_chat(chat_id=admin_id, text=text)

    def message_chat(self, chat_id: int, text: str):
        self.updater.bot.send_message(chat_id=chat_id, text=text)
        message_id = str(uuid4())
        message_content = {"message_content_type": "text", "text": text}
        from srai_chat.service.context_manager import ContextManager  # TODO

        service_persistency = ContextManager.get_instance().service_persistency
        service_persistency.dao_message.save_message(ChatMessage(message_id, str(chat_id), "0", "bot", message_content))
