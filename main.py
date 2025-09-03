import json
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


def create_intent(project_id, display_name, training_phrases, answer):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)

    training_phrases_list = []
    for phrase in training_phrases:
        part = dialogflow.Intent.TrainingPhrase.Part(text=phrase)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases_list.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=[answer])
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases_list,
        messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    return response


def train_intent(update: Update, context: CallbackContext):
    try:
        project_id = context.bot_data['project_id']

        with open('intent.json', 'r', encoding='utf-8') as file:
            intents_data = json.load(file)

        created_intents = []

        for intent_name, intent_data in intents_data.items():
            response = create_intent(
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
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Ошибка при создании интентов: {str(e)}"
        )


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
    dispatcher.bot_data['project_id'] = you_project_id


    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("train_intent", train_intent))
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    updater.start_polling()

if __name__ == "__main__":
    main()






