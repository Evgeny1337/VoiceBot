import os
import json
from dotenv import load_dotenv
from dialogflow_utils import create_intent



def train_intent(project_id, intent_file):
    try:
        with open(intent_file, 'r', encoding='utf-8') as file:
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
            return f"Созданы интенты: {', '.join(created_intents)}"
    except Exception as e:
        return f"Ошибка создание интентов {e}"


def main():
    load_dotenv(override=True)
    project_id = os.getenv("YOUR_PROJECT_ID")
    intent_file = os.getenv("INTENT_FILE")
    print(train_intent(project_id, intent_file))


if __name__ == '__main__':
    main()