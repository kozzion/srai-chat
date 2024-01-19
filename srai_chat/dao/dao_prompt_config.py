import json
from hashlib import sha256
from typing import Dict, List, Optional

from srai_chat.dao.dao_mongo_base import DaoMongoBase


class PromptConfig:
    def __init__(self, model: str, list_message: List[Dict[str, str]]):
        self.model = model
        self.list_message = list_message

    def to_dict(self) -> dict:
        return {
            "model": self.model,
            "list_message": self.list_message,
        }

    def apppend_message(self, role: str, message_content: str) -> "PromptConfig":
        if role not in ["system", "user", "assistant"]:
            raise Exception(f"role {role} not in [system, user, assistant]")
        list_message = self.list_message.copy()
        list_message.append({"role": role, "content": message_content})
        return PromptConfig(self.model, list_message)

    def append_system_message(self, message_content: str) -> "PromptConfig":
        return self.apppend_message("system", message_content)

    def append_user_message(self, message_content: str) -> "PromptConfig":
        return self.apppend_message("user", message_content)

    def append_assistent_message(self, message_content: str) -> "PromptConfig":
        return self.apppend_message("assistant", message_content)

    @staticmethod
    def create(
        model: str,
        system_message_content: str,
    ) -> "PromptConfig":
        list_message = []
        list_message.append({"role": "system", "content": system_message_content})

        return PromptConfig(model, list_message)

    @staticmethod
    def from_dict(dict_prompt_config: dict) -> "PromptConfig":
        model = dict_prompt_config["model"]
        list_message = dict_prompt_config["list_message"]
        return PromptConfig(model, list_message)


class DaoPromptConfig(DaoMongoBase):
    def __init__(self, connection_string: str, database_name: str) -> None:
        super().__init__(connection_string, database_name, "prompt_config")

    def save_prompt_config_cached(self, prompt_config_input: PromptConfig, prompt_config_result: PromptConfig) -> None:
        id = sha256(json.dumps(prompt_config_input.to_dict()).encode("utf-8")).hexdigest()
        self.save_prompt_config(id, prompt_config_result)

    def save_prompt_config(self, id: str, prompt_config_result: PromptConfig) -> None:
        prompt_config_result_dict = prompt_config_result.to_dict()
        prompt_config_result_dict["_id"] = id
        self.update_one({"_id": id}, {"$set": prompt_config_result_dict}, upsert=True)

    def load_prompt_config_cached(self, prompt_config_input: PromptConfig) -> Optional[PromptConfig]:
        id = sha256(json.dumps(prompt_config_input.to_dict()).encode("utf-8")).hexdigest()
        return self.load_prompt_config(id)

    def load_prompt_config(self, id: str) -> Optional[PromptConfig]:
        query = {"_id": id}
        result = self.find(query)
        # convert curser to list
        list_result = list(result)
        if len(list_result) == 0:
            return None
        else:
            dict_prompt_config = list_result[0]
            return PromptConfig.from_dict(dict_prompt_config)

    def load_prompt_config_all(self) -> List[dict]:
        return self.find({})  # type: ignore
