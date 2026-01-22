import json

from client import Client

if __name__ == "__main__":
    api = Client()

    user_key = api.user_key

    try:
        print(f"Запрос данных для: {user_key}")
        result = api.get_profile(key=user_key)

        formatted_json = json.dumps(
            result,
            indent=4,
            ensure_ascii=False
        )

        print(formatted_json)

    except Exception as e:
        print(f"Произошла ошибка при получении данных: {e}")
