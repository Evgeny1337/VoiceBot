import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CallbackContext, Updater, MessageHandler, Filters, CommandHandler

def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Здравствуйте')


def main():
    load_dotenv(override=True)
    token = str(os.getenv("TELEGRAM_TOKEN"))
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text,echo))
    updater.start_polling()



if __name__ == '__main__':
    main()
