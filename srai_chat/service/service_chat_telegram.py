from uuid import uuid4

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater

from srai_chat.command_base import CommandBase
from srai_chat.dao.dao_chat_message import ChatMessage
from srai_chat.service.context_manager import ContextManager
from srai_chat.service.service_chat_base import ServiceChatBase


class ServiceChatTelegram(ServiceChatBase):
    def __init__(
        self,
        context: ContextManager,
        bot_token: str,
        root_id: int,
    ):
        super().__init__(context, str(root_id))
        self.bot_token = bot_token
        # Create the Updater and pass it your bot's token.
        # Make sure to set use_context=True to use the new context based callbacks
        # Post version 12 this will no longer be necessary

        self.updater = Updater(self.bot_token, use_context=True)
        self.root_id = root_id
        self.list_admin_ids = [root_id]

    def initialize(self):
        super().initialize()
        self.updater.dispatcher.add_handler(CommandHandler("help", self.help))

        self.updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.handle_text_telegram))
        # self.updater.dispatcher.add_handler(CommandHandler("chat_id", self.chat_id))

    def start(self):
        # send a message to jaap about update
        from srai_chat.skill.skill_image_tag import image_tag

        self.message_admins(f"Startup succes with image tag {image_tag()}")
        #
        #  Start the Bot
        self.updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        # TODO have this come from
        self.updater.idle()

    def help(self, update: Update, context: CallbackContext):
        """Send a message when the command /help is issued."""
        message = "Available commands:\n"
        message += "/help\n"

        for command in self.dict_command.keys():
            message += f"/{command}\n"
        update.message.reply_text(message)

    def chat_id(self, update: Update, context: CallbackContext):
        """Send a message when the command /help is issued."""
        update.message.reply_text(str(update.message.chat_id))

    def error(self, update: Update, context: CallbackContext):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, context.error)

    def register_command(self, command: CommandBase):
        super().register_command(command)
        self.updater.dispatcher.add_handler(CommandHandler(command.command_name, command.execute_command_callback))

    def handle_text_telegram(self, update: Update, context: CallbackContext):
        """Handle text messages."""
        message_id = str(update.message.message_id)
        chat_id = str(update.message.chat_id)
        author_id = str(update.message.from_user.id)
        author_name = update.message.from_user.username
        if author_name is None:
            author_name = update.message.from_user.first_name
        if author_name is None:
            author_name = update.message.from_user.last_name
        if author_name is None:
            author_name = ""
        message_text = update.message.text

        self.handle_text(message_id, chat_id, author_id, author_name, message_text)

        # TODO move this to a skill or mode

    def message_chat(self, chat_id: str, text: str):
        if chat_id is None:
            raise Exception("chat_id is None")
        self.updater.bot.send_message(chat_id=str(chat_id), text=text)
        message_id = str(uuid4())
        message_content = {"message_content_type": "text", "text": text}
        self.context.service_persistency.dao_message.save_message(
            ChatMessage(message_id, chat_id, "0", "bot", message_content)
        )
