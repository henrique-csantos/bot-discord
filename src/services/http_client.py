import os
import aiohttp
import asyncio
from aiohttp import ClientResponseError, TCPConnector
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


def get_session() -> aiohttp.ClientSession:
    global _session

    if _session is None or _session.closed:
        connector = TCPConnector(limit=20, enable_cleanup_closed=True)
        _session = aiohttp.ClientSession(
            headers=HEADERS,
            connector=connector
        )

    return _session


async def fetch_with_retry(
    session: aiohttp.ClientSession,
    method: str,
    url: str,
    *,
    params: dict | None = None,
    retries: int = 3
):
    delay = 1

    for attempt in range(retries):
        try:
            async with session.request(
                method,
                url,
                params=params,
                timeout=aiohttp.ClientTimeout(total=15)
            ) as resp:
                resp.raise_for_status()
                return await resp.json()

        except (asyncio.TimeoutError, ClientResponseError):
            if attempt == retries - 1:
                raise
            await asyncio.sleep(delay)
            delay *= 2
