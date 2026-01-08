import requests
import json

from constants import BASE_URL, GET_PROFILE, GET_PERSON, GET_BIO, DEFAULT_KEY


def get_profile(key: str = DEFAULT_KEY, base_url: str = BASE_URL, timeout: int = 10):
    
    params = {
    'action': GET_PROFILE,
    'key': key
    }

    response = requests.get(base_url, params=params, timeout=timeout)
    response.raise_for_status()

    return response.json()

def get_person(key: str = DEFAULT_KEY, base_url: str = BASE_URL, timeout: int = 10):

    params = {
        'action': GET_PERSON,
        'key': key
    }

    response = requests.get(base_url, params=params, timeout=timeout)
    response.raise_for_status()

    return response.json()

def get_bio(key: str = DEFAULT_KEY, base_url: str = BASE_URL, timeout: int = 10):
    
    params = {
    'action': GET_BIO,
    'key': key
    }

    response = requests.get(base_url, params=params, timeout=timeout)
    response.raise_for_status()

    return response.json()

if __name__ == "__main__":
    data = get_bio()
    print(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True))