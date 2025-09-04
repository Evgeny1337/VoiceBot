import os
from dotenv import load_dotenv
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from help import detect_intent_texts
from google.cloud import dialogflow

def echo(event, vk_api, language_code, session, session_client):
    fulfillment_text = detect_intent_texts(
        session_client=session_client,
        session=session,
        text=event.text,
        language_code=language_code
    )
    vk_api.messages.send(
        user_id=event.user_id,
        message=fulfillment_text,
        random_id=get_random_id()
    )



def main():
    load_dotenv(override=True)
    token = os.getenv("VK_TOKEN")
    you_project_id = os.getenv("YOUR_PROJECT_ID")
    language_code = os.getenv("LANGUAGE_CODE")
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(you_project_id, '123456789')


    vk_session = vk.VkApi(token=token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api, language_code, session, session_client)

if __name__ == "__main__":
    main()