import os
from abc import ABC
from copy import copy
from hashlib import sha256
from typing import Callable

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from srai_chat.command_base import CommandBase


class SkillBase(ABC):
    def __init__(self) -> None:
        self.skill_name = self.__class__.__name__
        self.command_dict = {}

        connection_string = os.environ["MONGODB_CONNECTION_STRING"]
        database_name = os.environ["MONGODB_DATABASE_NAME"]
        # Create a new client and connect to the server
        self.client = MongoClient(connection_string, server_api=ServerApi("1"))
        self.db = self.client.get_database(database_name)
        self.collection = self.db.get_collection("skill_state")

        from srai_chat.service.context_manager import ContextManager  # avoiding circular import

        self.context: ContextManager = ContextManager.get_instance()

    def add_command(self, command: CommandBase) -> None:
        self.command_dict[command.command_name] = command

    def get_command_dict(self) -> dict:
        return copy(self.command_dict)

    def has_command_audio(self) -> bool:
        return False

    def get_command_audio(self) -> Callable:
        raise NotImplementedError()
