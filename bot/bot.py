import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    CallbackQueryHandler,
)
from bot.admin import Admin
from bot.questionnaire import Questionnaire


class Bot:
    def __init__(self):
        self.updater = Updater(token=os.getenv("TELEGRAM_TOKEN"))
        self.dispatcher = self.updater.dispatcher

        # Initialize administrator and questionnaire
        self.admin = Admin()
        self.questionnaire = Questionnaire()

        # Register command handlers
        self.dispatcher.add_handler(CommandHandler("start", self.start))

        self.dispatcher.add_handler(CommandHandler("admin", self.admin.handle))
        self.dispatcher.add_handler(
            MessageHandler(Filters.text & ~Filters.command, self.handle_message)
        )

    def start(self, update: Update, context: CallbackContext):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Привет! Я бот для подачи анкеты актерами. Начнем?",
        )

    def handle_message(self, update: Update, context: CallbackContext):
        # Pass message to admin or questionnaire depending on user status
        if self.admin.is_admin(update.effective_user.id):
            self.admin.handle_message(update, context)
        else:
            self.questionnaire.handle_message(update, context)

    def handle_language_selection(self, update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()
        language = query.data
        self.questionnaire.set_language(language)
        query.edit_message_text(text="Language selected: " + language)

    def run(self):
        self.updater.start_polling()
