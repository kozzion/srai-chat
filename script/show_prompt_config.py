import json

from srai_chat.service.context_manager import ContextManager

ContextManager.initialize_test_chat()
doa = ContextManager.get_instance().service_persistency.dao_prompt_config
list_prompt_config = doa.load_prompt_config_all()
for prompt_config in list_prompt_config:
    print(json.dumps(prompt_config, indent=4))
    print()
