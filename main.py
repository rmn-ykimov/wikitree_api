import json

from client import get_credentials, get_profile, prepare_session

if __name__ == "__main__":
    # 1. Получаем логин и пароль (из консоли или переменных окружения)
    email, password = get_credentials()

    # 2. Создаем сессию и проходим аутентификацию
    session = prepare_session(email, password)

    # 3. Вызываем функцию получения профиля, передавая сессию
    # По умолчанию используется DEFAULT_KEY из constants.py
    try:
        profile_data = get_profile(session)
        print("Данные профиля:")
        result = get_profile(session)

        formatted_json = json.dumps(
            result,
            indent=4,
            ensure_ascii=False
        )

        print(formatted_json)

    except Exception as e:
        print(f"Произошла ошибка при получении данных: {e}")
