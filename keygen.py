import os
from google.cloud import api_keys_v2
from google.cloud.api_keys_v2 import Key
from dotenv import load_dotenv

def create_api_key(project_id: str, suffix: str) -> Key:
    client = api_keys_v2.ApiKeysClient()

    key = api_keys_v2.Key()
    key.display_name = suffix

    request = api_keys_v2.CreateKeyRequest()
    request.parent = f"projects/{project_id}/locations/global"
    request.key = key

    response = client.create_key(request=request).result()

    return response

def main():
    load_dotenv(override=True)
    project_id = os.getenv("YOUR_PROJECT_ID")
    print(f"Введите наименование для ключа проекта {project_id}")
    key_suffix = input()
    if key_suffix:
        api_key = create_api_key(project_id, key_suffix)
        key_name = api_key.name
        print(f"Successfully created an API key: {key_name}")
    else:
        print('Вы не ввели наименование для ключа')

if __name__ == "__main__":
    main()


