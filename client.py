import json
import os
import re
import urllib.parse
from getpass import getpass

from requests import Session

from constants import (
    BASE_URL,
    CLIENT_LOGIN,
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
)

SESSION_FILE_PATH = os.path.join(os.path.dirname(__file__), ".wikitree_session.json")


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

    if not resp.ok:
        print("Cannot authenticate with Wikitree API: failed the authcode verification")
        exit()

    result_json = resp.json()
    login_data = result_json.get("clientLogin", {})
    user_name = login_data.get("username", "Unknown")

    if user_name != "Unknown":
        session.cookies.set("wikidb_wtb_UserName", urllib.parse.quote(user_name), domain="api.wikitree.com")
    else:
        cookies = session.cookies.get_dict()
        user_name = urllib.parse.unquote(cookies.get("wikidb_wtb_UserName", "Unknown"))

    print(f'User "{user_name}" is successfully authenticated!')


def save_session(session: Session) -> None:
    """Saves session cookies to a JSON file with restricted permissions."""
    cookies = session.cookies.get_dict()
    try:
        with open(SESSION_FILE_PATH, "w") as f:
            json.dump(cookies, f)
        os.chmod(SESSION_FILE_PATH, 0o600)
    except Exception as e:
        print(f"Warning: Could not save session: {e}")


def load_session(session: Session) -> bool:
    """Loads session cookies from a JSON file. Returns True if successful."""
    if not os.path.exists(SESSION_FILE_PATH):
        return False

    try:
        with open(SESSION_FILE_PATH, "r") as f:
            cookies = json.load(f)
            for name, value in cookies.items():
                session.cookies.set(name, value, domain="api.wikitree.com")
        return True
    except Exception as e:
        print(f"Warning: Could not load session: {e}")
        return False


def prepare_session(email: str | None = None, password: str | None = None) -> Session:
    """
    Prepares the session for the communication with Wikitree API,
    for authenticated access to API, fill in optional fields: email & password
    """

    session: Session = Session()

    # 1. Try to load existing session
    if load_session(session):
        # Verify session is still valid by attempting a simple call
        try:
            user_cookie = session.cookies.get("wikidb_wtb_UserName")
            if not user_cookie:
                raise Exception("Missing session cookies")

            user_key = urllib.parse.unquote(user_cookie)
            Client(session).get_profile(key=user_key)

            print(f"Session for user \"{user_key}\" loaded from cache and verified.")
            return session
        except Exception as e:
            if hasattr(e, 'response') and e.response is not None and e.response.status_code == 429:
                print("Rate limit exceeded (429). Please wait a few minutes and try again.")
                return session

            print(f"Cached session expired or invalid ({e}). Re-authenticating...")
            session.cookies.clear()

    # 2. If no valid session, authenticate
    # If credentials aren't provided, we'll need to fetch them
    if not email or not password:
        email, password = get_credentials()

    authenticate_session(session, email, password)
    save_session(session)

    return session

class Client:

    def __init__(self, session: Session):
        self.session = session

    def _post(self, action: str, **kwargs):
        data = {"action": action, **kwargs}
        response = self.session.post(BASE_URL, data=data, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_profile(self, key: str = DEFAULT_KEY):
        return self._post(GET_PROFILE, key=key)

    def get_person(self, key: str = DEFAULT_KEY):
        return self._post(GET_PERSON, key=key)

    def get_bio(self, key: str = DEFAULT_KEY):
        return self._post(GET_BIO, key=key)

    def get_photos(self, key: str = DEFAULT_KEY):
        return self._post(GET_PHOTOS, key=key)

    def get_people(self, key: str = DEFAULT_KEY):
        return self._post(GET_PEOPLE, key=key)

    def get_ancestors(self, key: str = DEFAULT_KEY):
        return self._post(GET_ANCESTORS, key=key)

    def get_descendants(self, key: str = DEFAULT_KEY):
        return self._post(GET_DESCENDANTS, key=key)

    def get_relatives(self, key: str = DEFAULT_KEY):
        return self._post(GET_RELATIVES, key=key)

    def get_watchlist(self, key: str = DEFAULT_KEY):
        return self._post(GET_WATCHLIST, key=key)

    def get_dna_tests_by_test_taker(self, key: str = DEFAULT_KEY):
        return self._post(GET_DNA_TESTS_BY_TEST_TAKER, key=key)

    def get_connected_profiles_by_dna_test(self, key: str = DEFAULT_KEY):
        return self._post(GET_CONNECTED_PROFILES_BY_DNA_TEST, key=key)

    def get_connected_dna_tests_by_profile(self, key: str = DEFAULT_KEY):
        return self._post(GET_CONNECTED_DNA_TESTS_BY_PROFILE, key=key)

    def get_categories(self, key: str = DEFAULT_KEY):
        return self._post(GET_CATEGORIES, key=key)

    def search_person(self, key: str = DEFAULT_KEY):
        return self._post(SEARCH_PERSON, key=key)