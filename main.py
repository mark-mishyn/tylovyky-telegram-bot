import os

from dotenv import load_dotenv

# have to load env before imports from our database module
load_dotenv()

from telegram import Update
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)

from bot.admin import Admin
from bot.questionnaire import Questionnaire


def main():
    print('---Bot started---')

    admin = Admin()
    questionnaire = Questionnaire()

    def start(update: Update, context: CallbackContext):
        if admin.is_admin(update.effective_user.id):
            admin.handle(update, context)
        else:
            questionnaire.start(update, context)

    def restart(update: Update, context: CallbackContext):
        if admin.is_admin(update.effective_user.id):
            admin.handle(update, context)
        else:
            # TODO check questionnaire.restart!
            questionnaire.restart(update, context)

    def handle_message(update: Update, context: CallbackContext):
        if admin.is_admin(update.effective_user.id):
            admin.handle_message(update, context)
        else:
            questionnaire.handle_message(update, context)

    def handle_photo(update: Update, context: CallbackContext):
        questionnaire.handle_photo(update, context)

    def handle_admin_callback_query(update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()
        if query.data == "show_all":
            admin.show_all(update, context)
        elif query.data == "search":
            context.user_data["search"] = True
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Enter a keyword:"
            )
        else:
            # Обработка других случаев query.data
            pass

    updater = Updater(token=os.getenv("TELEGRAM_TOKEN"), use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("restart", restart))
    admin_callback_query_handler = CallbackQueryHandler(
        handle_admin_callback_query, pattern="^(show_all|search)$"
    )
    dispatcher.add_handler(admin_callback_query_handler)
    callback_query_handler = CallbackQueryHandler(questionnaire.handle_callback_query)
    dispatcher.add_handler(callback_query_handler)
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, handle_message)
    )
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_photo))

    updater.start_polling()


if __name__ == "__main__":
    main()
