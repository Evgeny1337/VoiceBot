import os
import logging
from google.cloud import dialogflow
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CallbackContext, Updater, MessageHandler, Filters, CommandHandler
from dialogflow_utils import detect_intent_texts
from logger import setup_logging

logger = logging.getLogger(__name__)


def send_message(update: Update, context: CallbackContext):
    try:
        session_client = context.bot_data['session_client']
        project_id = context.bot_data['project_id']
        user_id = update.message.from_user.id
        session_id = f'tg-{user_id}'""
        session = session_client.session_path(project_id, session_id)
        language_code = context.bot_data['language_code']
        fulfillment_text = detect_intent_texts(
            session_client=session_client,
            session=session,
            text=update.message.text,
            language_code=language_code
        )
        if fulfillment_text:
            context.bot.send_message(chat_id=update.effective_chat.id, text=fulfillment_text)
    except Exception:
        logger.exception(f"Ошибка в send_message")
        raise


def start(update: Update, context: CallbackContext):
    try:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Здравствуйте')
    except Exception:
        logger.exception(f"Ошибка в start")
        raise




def main():
    try:
        load_dotenv(override=True)

        tg_token = os.getenv("TELEGRAM_TOKEN")
        tg_logs_token=os.getenv("TELEGRAM_LOGS_TOKEN")
        log_chat_id = os.getenv("TG_LOG_CHAT_ID")
        setup_logging(tg_logs_token, log_chat_id)

        logger.info("Запуск Telegram бота...")

        you_project_id = os.getenv("YOUR_PROJECT_ID")
        language_code = os.getenv("LANGUAGE_CODE")
        session_client = dialogflow.SessionsClient()

        updater = Updater(tg_token, use_context=True)
        dispatcher = updater.dispatcher

        dispatcher.bot_data['session_client'] = session_client
        dispatcher.bot_data['language_code'] = language_code
        dispatcher.bot_data['project_id'] = you_project_id

        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(MessageHandler(Filters.text, send_message))


        updater.start_polling()
        logger.info("Telegram бот запущен успешно")

    except Exception:
        logger.exception(f"Критическая ошибка при запуске бота")
        raise


if __name__ == "__main__":
    main()

