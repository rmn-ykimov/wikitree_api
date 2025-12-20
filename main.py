import requests
import json

from constants import BASE_URL, GET_PROFILE

KEY = "Romanov-62"

params = {
    'action': GET_PROFILE,
    'key': KEY
}

if __name__ == "__main__":
    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True))
