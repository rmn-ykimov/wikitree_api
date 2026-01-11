from requests import Session
import os
import re
import urllib.parse
from getpass import getpass


from constants import (
    BASE_URL,
    DEFAULT_KEY,
    GET_ANCESTORS,
    GET_BIO,
    GET_CATEGORIES,
    GET_CONNECTED_DNA_TESTS_BY_PROFILE,
    GET_CONNECTED_PROFILES_BY_DNA_TEST,
    GET_DESCENDANTS,
    GET_DNA_TESTS_BY_TEST_TAKER,
    GET_PEOPLE,
    GET_PERSON,
    GET_PHOTOS,
    GET_PROFILE,
    GET_RELATIVES,
    GET_WATCHLIST,
    SEARCH_PERSON,
    CLIENT_LOGIN,
)


def get_credentials() -> tuple[str, str]:
    """
    Loads credentials from environment variables (if provided), otherwise asks
    user for them.
    """

    email = os.environ.get("LOGIN_EMAIL") or input("Email: ")
    password = os.environ.get("LOGIN_PASSWORD") or getpass("Password: ")

    return email, password


def authenticate_session(session: Session, email: str, password: str) -> None:
    """Authenticates the session with provided credentials"""

    # Step 1: Obtain the authcode
    data = {
        "action": CLIENT_LOGIN,
        "doLogin": 1,
        "wpEmail": email,
        "wpPassword": password,
    }

    resp = session.post(
        BASE_URL,
        data=data,
        allow_redirects=False,
    )

    resp.raise_for_status()

    if (
        resp.status_code != 302
        or (location := resp.headers.get("Location")) is None
        or "authcode" not in location
    ):
        print("Cannot authenticate with Wikitree API: authcode was not obtained")
        exit()

    matches = re.search(r"authcode=(?P<authcode>.+$)", location).groupdict()
    authcode = matches.get("authcode")

    # Step 2: Send back the authcode to finish the authentication
    data = {"action": CLIENT_LOGIN, "authcode": authcode}

    resp = session.post(BASE_URL, data=data, allow_redirects=False)

    resp.raise_for_status()

    result_json = resp.json()
    login_data = result_json.get("clientLogin", {})

    if login_data.get("result") != "Success":
        print(f"Authentication failed: {login_data.get('result')}")
        exit()

    user_name = login_data.get("username")

    if user_name:
        safe_user_name = urllib.parse.quote(user_name)
        session.cookies.set(
            "wikidb_wtb_UserName", safe_user_name, domain="api.wikitree.com"
        )

    print(f'User "{user_name}" is successfully authenticated!')


def prepare_session(email: str | None, password: str | None) -> Session:
    """
    Prepares the session for the communication with Wikitree API,
    for authenticated access to API, fill in optional fields: email & password
    """

    session: Session = Session()

    session.headers.update({
        'User-Agent': 'TestWikiTreeApp'
    })

    if email and password:
        authenticate_session(session, email, password)

    return session

def get_profile(session:Session, key: str = DEFAULT_KEY, base_url: str = BASE_URL, timeout: int = 10):
    params = {"action": GET_PROFILE, "key": key}

    response = session.get(base_url, params=params, timeout=timeout)
    response.raise_for_status()

    return response.json()


def get_person(session: Session, key: str = DEFAULT_KEY, base_url: str = BASE_URL, timeout: int = 10):
    params = {"action": GET_PERSON, "key": key}

    response = session.get(base_url, params=params, timeout=timeout)
    response.raise_for_status()

    return response.json()


def get_bio(session: Session, key: str = DEFAULT_KEY, base_url: str = BASE_URL, timeout: int = 10):
    params = {"action": GET_BIO, "key": key}

    response = session.get(base_url, params=params, timeout=timeout)
    response.raise_for_status()

    return response.json()


def get_photos(session: Session, key: str = DEFAULT_KEY, base_url: str = BASE_URL, timeout: int = 10):
    params = {"action": GET_PHOTOS, "key": key}

    response = session.get(base_url, params=params, timeout=timeout)
    response.raise_for_status()

    return response.json()


def get_people(session: Session, key: str = DEFAULT_KEY, base_url: str = BASE_URL, timeout: int = 10):
    params = {"action": GET_PEOPLE, "key": key}

    response = session.get(base_url, params=params, timeout=timeout)
    response.raise_for_status()

    return response.json()


def get_ancestors(session:Session, key: str = DEFAULT_KEY, base_url: str = BASE_URL, timeout: int = 10):
    params = {"action": GET_ANCESTORS, "key": key}

    response = session.get(base_url, params=params, timeout=timeout)
    response.raise_for_status()

    return response.json()


def get_descendants(
    session: Session, key: str = DEFAULT_KEY, base_url: str = BASE_URL, timeout: int = 10
):
    params = {"action": GET_DESCENDANTS, "key": key}

    response = session.get(base_url, params=params, timeout=timeout)
    response.raise_for_status()

    return response.json()


def get_relatives(session: Session, key: str = DEFAULT_KEY, base_url: str = BASE_URL, timeout: int = 10):
    params = {"action": GET_RELATIVES, "key": key}

    response = session.get(base_url, params=params, timeout=timeout)
    response.raise_for_status()

    return response.json()


def get_watchlist(session: Session, key: str = DEFAULT_KEY, base_url: str = BASE_URL, timeout: int = 10):
    params = {"action": GET_WATCHLIST, "key": key}

    response = session.get(base_url, params=params, timeout=timeout)
    response.raise_for_status()

    return response.json()


def get_dna_tests_by_test_taker(
    session: Session, key: str = DEFAULT_KEY, base_url: str = BASE_URL, timeout: int = 10
):
    params = {"action": GET_DNA_TESTS_BY_TEST_TAKER, "key": key}

    response = session.get(base_url, params=params, timeout=timeout)
    response.raise_for_status()

    return response.json()


def get_connected_profiles_by_dna_test(
    session: Session, key: str = DEFAULT_KEY, base_url: str = BASE_URL, timeout: int = 10
):
    params = {"action": GET_CONNECTED_PROFILES_BY_DNA_TEST, "key": key}

    response = session.get(base_url, params=params, timeout=timeout)
    response.raise_for_status()

    return response.json()


def get_connected_dna_tests_by_profile(
    session: Session, key: str = DEFAULT_KEY, base_url: str = BASE_URL, timeout: int = 10
):
    params = {"action": GET_CONNECTED_DNA_TESTS_BY_PROFILE, "key": key}

    response = session.get(base_url, params=params, timeout=timeout)
    response.raise_for_status()

    return response.json()


def get_categories(session: Session, key: str = DEFAULT_KEY, base_url: str = BASE_URL, timeout: int = 10):
    params = {"action": GET_CATEGORIES, "key": key}

    response = session.get(base_url, params=params, timeout=timeout)
    response.raise_for_status()

    return response.json()


def search_person(session: Session, key: str = DEFAULT_KEY, base_url: str = BASE_URL, timeout: int = 10):
    params = {"action": SEARCH_PERSON, "key": key}

    response = session.get(base_url, params=params, timeout=timeout)
    response.raise_for_status()

    return response.json()
