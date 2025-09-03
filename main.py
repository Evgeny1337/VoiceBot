import uuid
import os
from google.cloud import dialogflow
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CallbackContext, Updater, MessageHandler, Filters, CommandHandler


def echo(update: Update, context: CallbackContext):
    session_client = context.bot_data['session_client']
    session = context.bot_data['session']
    language_code = context.bot_data['language_code']
    fulfillment_text = detect_intent_texts(
        session_client=session_client,
        session=session,
        text=update.message.text,
        language_code=language_code
    )

    context.bot.send_message(chat_id=update.effective_chat.id, text=fulfillment_text)

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Здравствуйте')


def detect_intent_texts(session_client, session, text, language_code):
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result.fulfillment_text


def main():
    load_dotenv(override=True)
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if creds_path and os.path.isfile(creds_path):
        print(f"Файл учетных данных найден: {creds_path}")
    else:
        print("Ошибка: Файл учетных данных не найден по указанному пути!")
    you_project_id = os.getenv("YOUR_PROJECT_ID")
    language_code = os.getenv("LANGUAGE_CODE")
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(you_project_id, '123456789')

    token = str(os.getenv("TELEGRAM_TOKEN"))
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.bot_data['session_client'] = session_client
    dispatcher.bot_data['session'] = session
    dispatcher.bot_data['language_code'] = language_code


    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    updater.start_polling()

if __name__ == "__main__":
    main()






