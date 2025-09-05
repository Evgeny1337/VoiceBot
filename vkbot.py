import os
import logging
from dotenv import load_dotenv
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from dialogflow_utils import detect_intent_texts
from google.cloud import dialogflow
from logger import setup_logging

logger = logging.getLogger(__name__)


def send_message(event, vk_api, language_code, you_project_id, session_client):
    user_id = event.user_id
    session_id = f'vk-{user_id}'
    session = session_client.session_path(you_project_id, session_id)
    try:
        fulfillment_text = detect_intent_texts(
            session_client=session_client,
            session=session,
            text=event.text,
            language_code=language_code
        )
        if fulfillment_text:
            vk_api.messages.send(
                user_id=event.user_id,
                message=fulfillment_text,
                random_id=get_random_id()
            )
    except Exception as e:
        logger.error(f"Ошибка в VK echo: {str(e)}")
        raise


def main():
    try:
        load_dotenv(override=True)

        tg_token = os.getenv("TELEGRAM_LOGS_TOKEN")
        log_chat_id = os.getenv("TG_LOG_CHAT_ID")
        setup_logging(tg_token, log_chat_id)

        logger.info("Запуск VK бота...")

        token = os.getenv("VK_TOKEN")
        you_project_id = os.getenv("YOUR_PROJECT_ID")
        language_code = os.getenv("LANGUAGE_CODE")
        session_client = dialogflow.SessionsClient()

        vk_session = vk.VkApi(token=token)
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        logger.info("VK бот запущен успешно")
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                send_message(event, vk_api, language_code, you_project_id, session_client)
    except Exception as e:
        logger.critical(f"Критическая ошибка при запуске VK бота: {str(e)}")
        raise


if __name__ == "__main__":
    main()