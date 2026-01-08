import requests
import json

from constants import (BASE_URL, GET_PROFILE, GET_PERSON, GET_BIO, GET_PHOTOS,
                       GET_PEOPLE, GET_ANCESTORS, GET_DESCENDANTS,
                       GET_RELATIVES, GET_WATCHLIST,
                       GET_DNA_TESTS_BY_TEST_TAKER,
                       GET_CONNECTED_PROFILES_BY_DNA_TEST,
                       GET_CONNECTED_DNA_TESTS_BY_PROFILE, GET_CATEGORIES,
                       SEARCH_PERSON, DEFAULT_KEY)


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

def get_photos(key: str = DEFAULT_KEY, base_url: str = BASE_URL, timeout: int = 10):

    params = {
        'action': GET_PHOTOS,
        'key': key
    }

    response = requests.get(base_url, params=params, timeout=timeout)
    response.raise_for_status()

    return response.json()

def get_people(key: str = DEFAULT_KEY, base_url: str = BASE_URL, timeout: int = 10):

    params = {
        'action': GET_PEOPLE,
        'key': key
    }

    response = requests.get(base_url, params=params, timeout=timeout)
    response.raise_for_status()

    return response.json()

def get_ancestors(key: str = DEFAULT_KEY, base_url: str = BASE_URL, timeout: int = 10):

    params = {
        'action': GET_ANCESTORS,
        'key': key
    }

    response = requests.get(base_url, params=params, timeout=timeout)
    response.raise_for_status()

    return response.json()

def get_descendants(key: str = DEFAULT_KEY, base_url: str = BASE_URL, timeout: int = 10):

    params = {
        'action': GET_DESCENDANTS,
        'key': key
    }

    response = requests.get(base_url, params=params, timeout=timeout)
    response.raise_for_status()

    return response.json()

def get_relatives(key: str = DEFAULT_KEY, base_url: str = BASE_URL, timeout: int = 10):

    params = {
        'action': GET_RELATIVES,
        'key': key
    }

    response = requests.get(base_url, params=params, timeout=timeout)
    response.raise_for_status()

    return response.json()

def get_watchlist(key: str = DEFAULT_KEY, base_url: str = BASE_URL, timeout: int = 10):

    params = {
        'action': GET_WATCHLIST,
        'key': key
    }

    response = requests.get(base_url, params=params, timeout=timeout)
    response.raise_for_status()

    return response.json()

def get_dna_tests_by_test_taker(key: str = DEFAULT_KEY, base_url: str = BASE_URL, timeout: int = 10):

    params = {
        'action': GET_DNA_TESTS_BY_TEST_TAKER,
        'key': key
    }

    response = requests.get(base_url, params=params, timeout=timeout)
    response.raise_for_status()

    return response.json()

def get_connected_profiles_by_dna_test(key: str = DEFAULT_KEY, base_url: str = BASE_URL, timeout: int = 10):

    params = {
        'action': GET_CONNECTED_PROFILES_BY_DNA_TEST,
        'key': key
    }

    response = requests.get(base_url, params=params, timeout=timeout)
    response.raise_for_status()

    return response.json()

def get_connected_dna_tests_by_profile(key: str = DEFAULT_KEY, base_url: str = BASE_URL, timeout: int = 10):

    params = {
        'action': GET_CONNECTED_DNA_TESTS_BY_PROFILE,
        'key': key
    }

    response = requests.get(base_url, params=params, timeout=timeout)
    response.raise_for_status()

    return response.json()

def get_categories(key: str = DEFAULT_KEY, base_url: str = BASE_URL, timeout: int = 10):

    params = {
        'action': GET_CATEGORIES,
        'key': key
    }

    response = requests.get(base_url, params=params, timeout=timeout)
    response.raise_for_status()

    return response.json()

def search_person(key: str = DEFAULT_KEY, base_url: str = BASE_URL, timeout: int = 10):

    params = {
        'action': SEARCH_PERSON,
        'key': key
    }

    response = requests.get(base_url, params=params, timeout=timeout)
    response.raise_for_status()

    return response.json()

if __name__ == "__main__":
    data = get_bio()
    print(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True))