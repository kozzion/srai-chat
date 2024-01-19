from openai import OpenAI, chat

from srai_chat.dao.dao_prompt_config import PromptConfig
from srai_chat.mode_base import ModeBase
from srai_chat.service.service_openai_chat_gpt import ServiceChatGpt
from srai_chat.service.service_persistency import ServicePersistency


class ModeChatgpt(ModeBase):
    def __init__(self) -> None:
        super().__init__()

    # TODO figure out when to advance context
    #        if 0 < len(self.list_message_current):
    #            self.advance_context()

    def load_state(self, chat_id_str: str) -> "PromptConfig":
        ServicePersistency.get_instance().dao_prompt_config.load_prompt_config(chat_id_str
        dict_state = self.dao_state.find_one({"chat_id_str": chat_id_str})
        if dict_state is None:
            return ModeSupportState.create()
        else:
            return ModeSupportState.from_dict(dict_state["state"])

    # def save_state(self, chat_id_str: str, state: ModeSupportState) -> None:
    #     print("saving state")
    #     self.dao_state.update_one(
    #         {"chat_id_str": chat_id_str},
    #         {"$set": {"state": state.to_dict()}},
    #         upsert=True,
    #     )

    def process_message(self, chat_id: int, user_message_content: str) -> None:
        prompt_config = ServicePersistency.get_instance().dao_prompt_config.load_prompt_config(chat_id)
        if prompt_config is None:
            prompt_config = prompt_config.create("You are a helpfull assistent")
        promt_config = promt_config.append_user_message(user_message_content)
        ServiceChatGpt().prompt_simple(chat_id, promt_config)
        state = self.load_state(str(chat_id))
        if user_message_content == "":
            if 0 < len(state.list_message_current):
                if state.list_message_current[-1]["role"] == "assistant":
                    self.service_telegram_bot.message_chat(chat_id, state.list_message_current[-1]["content"])
                    return

        #        system_message += context_current_str
        # skill_state = self.skill.load_skill_state(chat_id)
        if len(state.list_message_current) == 0:
            state.list_message_current.append({"role": "system", "content": system_message_content})
        if user_message_content != "":
            state.list_message_current.append({"role": "user", "content": user_message_content})

        completion = self.client_openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=state.list_message_current,
        )
        assistent_message_content = completion.choices[0].message.content
        state.list_message_current.append({"role": "assistant", "content": assistent_message_content})
        self.service_telegram_bot.message_chat(chat_id, assistent_message_content)
        self.save_state(str(chat_id), state)
