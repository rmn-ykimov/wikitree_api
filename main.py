import json
import urllib.parse

from client import Client, prepare_session
from constants import DEFAULT_KEY

if __name__ == "__main__":
    session = prepare_session()

    user_cookie = session.cookies.get("wikidb_wtb_UserName")
    user_key = urllib.parse.unquote(user_cookie) if user_cookie else DEFAULT_KEY

    try:
        api = Client(session)
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
