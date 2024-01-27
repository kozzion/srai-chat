from hashlib import sha256

from srai_chat.dao.dao_base import DaoBase
from srai_chat.dao.store_document_base import StoreDocumentBase


class ModeState:
    def __init__(
        self,
        mode_state_id: str,
        payload: dict,
    ):
        if mode_state_id is None:
            raise Exception("mode_state_id is None")
        if payload is None:
            raise Exception("payload is None")

        self.mode_state_id = mode_state_id
        self.payload = payload

    def to_dict(self) -> dict:
        return {
            "mode_state_id": self.mode_state_id,
            "payload": self.payload,
        }

    @staticmethod
    def from_dict(dict_mode_state: dict) -> "ModeState":
        mode_state_id = dict_mode_state["mode_state_id"]
        payload = dict_mode_state["payload"]
        return ModeState(mode_state_id, payload)


class DaomodeState(DaoBase):
    def __init__(self, store_document: StoreDocumentBase) -> None:
        super().__init__(store_document)

    def get_id(self, mode_name: str, chat_id: str) -> str:
        if mode_name is None:
            raise Exception("mode_name is None")
        if mode_name == "":
            raise Exception("mode_name is empty")
        if chat_id is None:
            raise Exception("chat_id is None")
        if chat_id == "":
            raise Exception("chat_id is empty")
        text_key = f"{mode_name}_{chat_id}"
        hash_key = sha256(text_key.encode()).hexdigest()
        return hash_key

    def load_mode_state(self, mode_name: str, chat_id: str) -> ModeState:
        id = self.get_id(mode_name, chat_id)
        mode_state_dict = self.store_document.find({"_id": id})
        if mode_state_dict is None:
            return ModeState(id, {})
        else:
            return ModeState.from_dict(mode_state_dict[0])

    def save_mode_state(self, mode_name: str, chat_id: str, mode_state: ModeState) -> None:
        id = self.get_id(mode_name, chat_id)
        self.store_document.update_one({"_id": id}, {"$set": {"payload": mode_state.payload}}, upsert=True)
