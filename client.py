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

class Client:

    def __init__(self, email: str | None = None, password: str | None = None):
        """
        Initializes the WikiTree API client.

        Sets up a persistent session and prepares it by either loading from
        cache or authenticating.

        Args:
            email: Optional login email.
            password: Optional login password.
        """
        self.session = Session()
        self._prepare_session(email, password)

    def _prepare_session(
        self, email: str | None = None, password: str | None = None
    ) -> Session:
        """
        Prepares the session for communication with the WikiTree API.

        Attempts to load a cached session first. If no valid session is found,
        it authenticates using the provided credentials or prompts for them.

        Args:
            email: Optional login email.
            password: Optional login password.

        Returns:
            The prepared requests.Session object.
        """

        # 1. Try to load existing session
        if self._load_session():
            # Verify session is still valid by attempting a simple call
            error_msg = "Unknown error"
            try:
                user_cookie = self.session.cookies.get("wikidb_wtb_UserName")
                if not user_cookie:
                    raise Exception("Missing session cookies")

                user_key = urllib.parse.unquote(user_cookie)
                self.get_profile(key=user_key)

                print(
                    f"Session for user \"{user_key}\" "
                    "loaded from cache and verified."
                )
                return self.session
            except Exception as e:
                error_msg = str(e)
                if (
                    hasattr(e, "response")
                    and e.response is not None
                    and e.response.status_code == 429
                ):
                    print(
                        "Rate limit exceeded (429). "
                        "Please wait a few minutes and try again."
                    )
                    return self.session

            print(
                f"Cached session expired or invalid ({error_msg}). "
                "Re-authenticating..."
            )
            self.session.cookies.clear()

        # 2. If no valid session, authenticate
        # If credentials aren't provided, we'll need to fetch them
        if not email or not password:
            email, password = self._get_credentials()

        self._authenticate_session(email, password)
        self._save_session()

        return self.session

    def _save_session(self) -> None:
        """Saves session cookies to a JSON file with restricted permissions."""
        cookies = self.session.cookies.get_dict()
        try:
            with open(SESSION_FILE_PATH, "w") as f:
                json.dump(cookies, f)
            os.chmod(SESSION_FILE_PATH, 0o600)
        except Exception as e:
            print(f"Warning: Could not save session: {e}")

    def _load_session(self) -> bool:
        """
        Loads session cookies from a JSON file.

        Returns:
            True if session was loaded successfully, False otherwise.
        """
        if not os.path.exists(SESSION_FILE_PATH):
            return False

        try:
            with open(SESSION_FILE_PATH, "r") as f:
                cookies = json.load(f)
                for name, value in cookies.items():
                    self.session.cookies.set(
                        name, value, domain="api.wikitree.com"
                    )
            return True
        except Exception as e:
            print(f"Warning: Could not load session: {e}")
            return False

    def _authenticate_session(self, email: str, password: str) -> None:
        """
        Authenticates the session with the provided credentials.

        Follows the WikiTree API's two-step authentication process:
        1. POST credentials to get an authcode via a redirect.
        2. POST the authcode to verify and get session cookies.

        Args:
            email: User's login email.
            password: User's login password.
        """

        # Step 1: Obtain the authcode
        data = {
            "action": CLIENT_LOGIN,
            "doLogin": 1,
            "wpEmail": email,
            "wpPassword": password,
        }

        resp = self.session.post(
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
            print("Cannot authenticate with Wikitree API: authcode not obtained")
            exit()

        matches = re.search(r"authcode=(?P<authcode>.+$)", location).groupdict()
        authcode = matches.get("authcode")

        # Step 2: Send back the authcode to finish the authentication
        data = {"action": CLIENT_LOGIN, "authcode": authcode}

        resp = self.session.post(BASE_URL, data=data, allow_redirects=False)

        resp.raise_for_status()

        if not resp.ok:
            print("Cannot authenticate with Wikitree API: authcode verification failed")
            exit()

        result_json = resp.json()
        login_data = result_json.get("clientLogin", {})
        user_name = login_data.get("username", "Unknown")

        if user_name != "Unknown":
            self.session.cookies.set(
                "wikidb_wtb_UserName",
                urllib.parse.quote(user_name),
                domain="api.wikitree.com",
            )
        else:
            cookies = self.session.cookies.get_dict()
            user_name = urllib.parse.unquote(
                cookies.get("wikidb_wtb_UserName", "Unknown")
            )

        print(f'User "{user_name}" is successfully authenticated!')

    @staticmethod
    def _get_credentials() -> tuple[str, str]:
        """
        Loads credentials from environment variables (if provided), otherwise asks
        user for them.
        """

        email = os.environ.get("LOGIN_EMAIL") or input("Email: ")
        password = os.environ.get("LOGIN_PASSWORD") or getpass("Password: ")

        return email, password

    @property
    def user_key(self) -> str:
        """Returns the current authenticated user's key."""
        cookie = self.session.cookies.get("wikidb_wtb_UserName")
        return urllib.parse.unquote(cookie) if cookie else DEFAULT_KEY

    def _post(self, action: str, **kwargs):
        """Internal helper for making POST requests to the API."""
        data = {"action": action, **kwargs}
        response = self.session.post(BASE_URL, data=data, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_profile(self, key: str = DEFAULT_KEY):
        """Fetches profile information for a given person key."""
        return self._post(GET_PROFILE, key=key)

    def get_person(self, key: str = DEFAULT_KEY):
        """Fetches basic person data."""
        return self._post(GET_PERSON, key=key)

    def get_bio(self, key: str = DEFAULT_KEY):
        """Fetches the biography text for a person."""
        return self._post(GET_BIO, key=key)

    def get_photos(self, key: str = DEFAULT_KEY):
        """Fetches photos associated with a person."""
        return self._post(GET_PHOTOS, key=key)

    def get_people(self, key: str = DEFAULT_KEY):
        """Fetches multiple people's data."""
        return self._post(GET_PEOPLE, key=key)

    def get_ancestors(self, key: str = DEFAULT_KEY):
        """Fetches ancestors for a person."""
        return self._post(GET_ANCESTORS, key=key)

    def get_descendants(self, key: str = DEFAULT_KEY):
        """Fetches descendants for a person."""
        return self._post(GET_DESCENDANTS, key=key)

    def get_relatives(self, key: str = DEFAULT_KEY):
        """Fetches relatives for a person."""
        return self._post(GET_RELATIVES, key=key)

    def get_watchlist(self, key: str = DEFAULT_KEY):
        """Fetches the authenticated user's watchlist."""
        return self._post(GET_WATCHLIST, key=key)

    def get_dna_tests_by_test_taker(self, key: str = DEFAULT_KEY):
        """Fetches DNA tests for a test taker."""
        return self._post(GET_DNA_TESTS_BY_TEST_TAKER, key=key)

    def get_connected_profiles_by_dna_test(self, key: str = DEFAULT_KEY):
        """Fetches profiles connected to a DNA test."""
        return self._post(GET_CONNECTED_PROFILES_BY_DNA_TEST, key=key)

    def get_connected_dna_tests_by_profile(self, key: str = DEFAULT_KEY):
        """Fetches DNA tests connected to a profile."""
        return self._post(GET_CONNECTED_DNA_TESTS_BY_PROFILE, key=key)

    def get_categories(self, key: str = DEFAULT_KEY):
        """Fetches categories."""
        return self._post(GET_CATEGORIES, key=key)

    def search_person(self, key: str = DEFAULT_KEY):
        """Searches for a person."""
        return self._post(SEARCH_PERSON, key=key)
