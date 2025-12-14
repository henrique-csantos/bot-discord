import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()

BIBLIA_API_URL = os.getenv("BIBLIA_API_URL")
BIBLIA_API_KEY = os.getenv("BIBLIA_API_KEY")
APP_NAME = os.getenv("APP_NAME")
APP_VERSION = os.getenv("APP_VERSION")
CONTACT_INFO = os.getenv("CONTACT_INFO")

PROPRIETARY_USER_AGENT = f"{APP_NAME}/{APP_VERSION} ({CONTACT_INFO})"

HEADERS = {
    "User-Agent": PROPRIETARY_USER_AGENT,
    "Authorization": f"Bearer {BIBLIA_API_KEY}" if BIBLIA_API_KEY else "",
    "Accept": "application/json",
}

def get_session():
    return aiohttp.ClientSession(headers=HEADERS)
