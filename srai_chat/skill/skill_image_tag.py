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
    def __init__(self) -> None:
        super().__init__("image_tag", "Get the docker image tag of the image the bot is currently running")

    def execute_command(self, chat_id: str, command_message: str) -> dict:
        message = image_tag()
        from srai_chat.service.context_manager import ContextManager

        ContextManager.get_instance().service_chat.message_chat(chat_id, message)
        return {"image_tag": message}


class SkillImageTag(SkillBase):
    def __init__(self):
        super().__init__()
        self.add_command(CommandImageTag())
