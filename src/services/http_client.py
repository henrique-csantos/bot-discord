import os
import asyncio
import aiohttp
from aiohttp import ClientResponseError
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

_session: aiohttp.ClientSession | None = None

def get_session():
    global _session
    if _session is None or _session.closed:
        _session = aiohttp.ClientSession(headers=HEADERS)
    return _session

async def close_session():
    global _session
    if _session is not None and not _session.closed:
        await _session.close()
        _session = None

async def fetch_with_retry(session, method, url, *, params=None, retries=3):
    delay = 1

    for attempt in range(retries):
        try:
            async with session.request(method, url, params=params, timeout=10) as resp:
                resp.raise_for_status()
                return await resp.json()

        except (asyncio.TimeoutError, ClientResponseError) as e:
            if attempt == retries - 1:
                raise
            await asyncio.sleep(delay)
            delay *= 2

