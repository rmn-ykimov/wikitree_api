"""
This is a bare-bones example of authenticating as a "known" (not interactive
through a browser) WikiTree member for use with the WikiTree API. In order to
carry the authentication through a Session is maintained with
https://api.wikitree.com which holds the session state via cookie, as a browser
would.
"""

from requests import Session
import re
from getpass import getpass
import os

import urllib.parse
import json
from constants import BASE_URL, CLIENT_LOGIN


def get_credentials() -> tuple[str, str]:
    """
    Loads credentials from environment variables (if provided), otherwise asks
    user for them.
    """

    email = os.environ.get("LOGIN_EMAIL") or input("Email: ")
    password = os.environ.get("LOGIN_PASSWORD") or getpass(f"Password: ")

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
    data = {
        "action": CLIENT_LOGIN,
        "authcode": authcode
        }
    
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
            "wikidb_wtb_UserName",
            safe_user_name,
            domain="api.wikitree.com"
            )

    print(f'User "{user_name}" is successfully authenticated!')


def prepare_session(email: str | None, password: str | None) -> Session:
    """
    Prepares the session for the communication with Wikitree API,
    for authenticated access to API, fill in optional fields: email & password
    """

    session: Session = Session()

    if email and password:
        authenticate_session(session, email, password)

    return session


def load_profile(session: Session, key: str) -> dict[str, any]:
    """Loads the info for the user specified by the key parameter"""

    fields = "Id,Name,FirstName,LastNameAtBirth,LastNameCurrent,BirthDate"

    print(f"\nPOST /api.php?getProfile={key}fields={fields}\n")

    resp = session.post(
        BASE_URL,
        {"action": "getProfile", "key": key, "fields": fields}
        )
    
    resp.raise_for_status()

    return resp.json()


if __name__ == "__main__":
    # email, password = None, None # uncomment to test without authentication
    email, password = get_credentials()  # comment to test without authentication

    print(f"Starting the session as" + (f'"{email}"' if email else "unauthenticated user") + ".")
    session = prepare_session(email, password)

    # As an example, get the logged-in member's profile data itself
    key = session.cookies.get("wikidb_wtb_UserName") or "Windsor-1" # uses Windsor-1 when not authenticated
    profile = load_profile(session, urllib.parse.unquote(key))

    print(json.dumps(profile, indent=2, ensure_ascii=False))