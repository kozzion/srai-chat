from abc import ABC

from srai_chat.service.context_manager import ContextManager


class ServiceBase(ABC):
    def __init__(self, context: ContextManager):
        self.context = context

    def initialize(self) -> None:
        pass

    def start(self) -> None:
        pass
