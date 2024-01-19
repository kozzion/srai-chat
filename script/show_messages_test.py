import os

from srai_chat.dao.dao_chat_message import DaoChatMessage

connection_string = os.environ["MONGODB_CONNECTION_STRING"]
database_name = os.environ["MONGODB_DATABASE_NAME"]

dao_message = DaoChatMessage(connection_string, database_name)
print(dao_message.count())
list_message = dao_message.load_messages_all()
for message in list_message:
    print(message)
