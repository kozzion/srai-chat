from hashlib import sha256

from srai_chat.dao.dao_base import DaoBase
from srai_chat.dao.store_document_base import StoreDocumentBase


class SkillState:
    def __init__(
        self,
        skill_state_id: str,
        payload: dict,
    ):
        if skill_state_id is None:
            raise Exception("skill_state_id is None")
        if payload is None:
            raise Exception("payload is None")

        self.payload = payload
        self.skill_state_id = skill_state_id

    def to_dict(self) -> dict:
        return {
            "skill_state_id": self.skill_state_id,
            "payload": self.payload,
        }

    @staticmethod
    def from_dict(dict_skill_state: dict) -> "SkillState":
        skill_state_id = dict_skill_state["skill_state_id"]
        payload = dict_skill_state["payload"]
        return SkillState(skill_state_id, payload)


class DaoSkillState(DaoBase):
    def __init__(self, store_document: StoreDocumentBase) -> None:
        super().__init__(store_document)

    def get_id(self, skill_name: str, chat_id: str) -> str:
        if skill_name is None:
            raise Exception("skill_name is None")
        if skill_name == "":
            raise Exception("skill_name is empty")
        if chat_id is None:
            raise Exception("chat_id is None")
        if chat_id == "":
            raise Exception("chat_id is empty")
        text_key = f"{skill_name}_{chat_id}"
        hash_key = sha256(text_key.encode()).hexdigest()
        return hash_key

    def load_skill_state(self, skill_name: str, chat_id: str) -> SkillState:
        id = self.get_id(skill_name, chat_id)
        skill_state_dict = self.store_document.find({"_id": id})
        if skill_state_dict is None:
            return SkillState(id, {})
        else:
            return SkillState.from_dict(skill_state_dict[0])

    def save_skill_state(self, skill_name: str, chat_id: str, skill_state: SkillState) -> None:
        id = self.get_id(skill_name, chat_id)
        self.store_document.update_one({"_id": id}, {"$set": {"payload": skill_state.payload}}, upsert=True)
