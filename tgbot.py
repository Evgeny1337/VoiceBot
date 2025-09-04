import json
import os
import logging
from google.cloud import dialogflow
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CallbackContext, Updater, MessageHandler, Filters, CommandHandler
from help import detect_intent_texts, create_intent
from logger import setup_logging

logger = logging.getLogger(__name__)


def echo(update: Update, context: CallbackContext):
    try:
        session_client = context.bot_data['session_client']
        session = context.bot_data['session']
        language_code = context.bot_data['language_code']
        fulfillment_text = detect_intent_texts(
            session_client=session_client,
            session=session,
            text=update.message.text,
            language_code=language_code
        )
        if fulfillment_text:
            context.bot.send_message(chat_id=update.effective_chat.id, text=fulfillment_text)
    except Exception as e:
        logger.error(f"Ошибка в echo: {str(e)}")
        raise


def start(update: Update, context: CallbackContext):
    try:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Здравствуйте')
    except Exception as e:
        logger.error(f"Ошибка в start: {str(e)}")
        raise


def train_intent(update: Update, context: CallbackContext):
    try:
        project_id = context.bot_data['project_id']
        with open('intent.json', 'r', encoding='utf-8') as file:
            intents_data = json.load(file)
        created_intents = []
        for intent_name, intent_data in intents_data.items():
            create_intent(
                project_id=project_id,
                display_name=intent_name,
                training_phrases=intent_data['questions'],
                answer=intent_data['answer']
            )
            created_intents.append(intent_name)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Созданы интенты: {', '.join(created_intents)}"
        )
    except Exception as e:
        logger.error(f"Ошибка в train_intent: {str(e)}")
        raise


def error_handler(update: Update, context: CallbackContext):
    logger.error(f"Ошибка в обработчике: {context.error}")


def main():
    try:
        load_dotenv(override=True)

        tg_token = os.getenv("TELEGRAM_TOKEN")
        log_chat_id = os.getenv("TG_LOG_CHAT_ID")
        setup_logging(tg_token, log_chat_id)

        logger.info("Запуск Telegram бота...")

        you_project_id = os.getenv("YOUR_PROJECT_ID")
        language_code = os.getenv("LANGUAGE_CODE")
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(you_project_id, '123456789')

        updater = Updater(tg_token, use_context=True)
        dispatcher = updater.dispatcher

        dispatcher.bot_data['session_client'] = session_client
        dispatcher.bot_data['session'] = session
        dispatcher.bot_data['language_code'] = language_code
        dispatcher.bot_data['project_id'] = you_project_id

        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("train_intent", train_intent))
        dispatcher.add_handler(MessageHandler(Filters.text, echo))
        dispatcher.add_error_handler(error_handler)

        updater.start_polling()
        logger.info("Telegram бот запущен успешно")

    except Exception as e:
        logger.critical(f"Критическая ошибка при запуске бота: {str(e)}")
        raise


if __name__ == "__main__":
    main()