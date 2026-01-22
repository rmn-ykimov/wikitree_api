import json
import urllib.parse
from constants import DEFAULT_KEY
from client import get_profile, prepare_session

if __name__ == "__main__":
    session = prepare_session()

    user_cookie = session.cookies.get("wikidb_wtb_UserName")
    user_key = urllib.parse.unquote(user_cookie) if user_cookie else DEFAULT_KEY

    try:
        print(f"Запрос данных для: {DEFAULT_KEY}")
        result = get_profile(session, key=DEFAULT_KEY)

        formatted_json = json.dumps(
            result,
            indent=4,
            ensure_ascii=False
        )

        print(formatted_json)

    except Exception as e:
        print(f"Произошла ошибка при получении данных: {e}")
