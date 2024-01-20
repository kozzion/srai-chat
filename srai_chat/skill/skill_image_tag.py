import os

from srai_chat.command_base import CommandBase
from srai_chat.skill_base import SkillBase


def image_tag() -> str:
    message = ""
    image_tag = os.environ.get("IMAGE_TAG")
    if image_tag is None:
        message = "IMAGE_TAG not set"
    else:
        message = f"{image_tag}"
    return message


class CommandImageTag(CommandBase):
    def __init__(self, skill: SkillBase) -> None:
        super().__init__(skill, "image_tag")

    def execute_command(self, chat_id: str, command_message: str) -> None:
        message = image_tag()
        from srai_chat.service.context_manager import ContextManager

        ContextManager.get_instance().service_chat.message_chat(chat_id, message)


class SkillImageTag(SkillBase):
    def __init__(self):
        super().__init__()
        self.add_command(CommandImageTag(self))
