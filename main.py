import json
import pathlib

import database
from client import Client
from constants import DEFAULT_KEY

if __name__ == "__main__":
    database.init_db()
    api = Client()

    # user_key = api.user_key
    user_key = DEFAULT_KEY

    try:
        print(f"Запрос данных для: {user_key}")
        result = api.get_profile(key=user_key)

        if result and isinstance(result, list) and len(result) > 0:
            profile_data = result[0]
            page_name = profile_data.get("page_name")
            profile = profile_data.get("profile", {})
            first_name = profile.get("FirstName")
            last_name = profile.get("LastNameAtBirth")

            birth_date = profile.get("BirthDate") or ""
            birth_year = int(birth_date.split("-")[0]) if "-" in birth_date and birth_date.split("-")[0].isdigit() else None

            death_date = profile.get("DeathDate") or ""
            death_year = int(death_date.split("-")[0]) if "-" in death_date and death_date.split("-")[0].isdigit() else None

            if page_name:
                database.save_profile(page_name, first_name, last_name, birth_year, death_year)
                print(f"Профиль {page_name} ({first_name} {last_name}) успешно сохранен в базу!")
            else:
                print("В ответе API не найден page_name для сохранения в БД.")

        formatted_json = json.dumps(
            result,
            indent=4,
            ensure_ascii=False
        )

        pathlib.Path("data.json").write_text(formatted_json, encoding="utf-8")

        # print(formatted_json)

    except Exception as e:
        print(f"Произошла ошибка: {e}")
