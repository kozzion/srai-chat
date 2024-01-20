from srai_chat.service.context_manager import ContextManager

ContextManager.initialize_test_chat()
dao = ContextManager.get_instance().service_persistency.dao_prompt_config
count = dao.count()
print(f"count: {count}")
delete_count = dao.delete_all()
print(f"delete_count: {delete_count}")
count = dao.count()
print(f"count: {count}")
