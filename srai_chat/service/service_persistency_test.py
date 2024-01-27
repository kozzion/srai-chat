from srai_chat.service.context_manager import ContextManager
from srai_chat.service.service_base import ServiceBase


class ServicePersistencyTest(ServiceBase):
    def __init__(self, context: ContextManager):
        super().__init__(context)
        # daos
        self.dao_message = None
        self.dao_prompt_config = None
        self.dao_skill_state = None
        self.dao_mode_state = None
