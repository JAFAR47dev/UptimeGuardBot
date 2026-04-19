# services/checker.py
import aiohttp
import asyncio
import time
import ssl
import socket
from urllib.parse import urlparse

BODY_READ_LIMIT = 50_000   # bytes — enough for keyword checks without wasting memory


async def check_url(
    url: str,
    session: aiohttp.ClientSession = None,
    keyword: str = None,
    keyword_case_sensitive: bool = False,
) -> dict:
    """
    Ping a URL and return status, response time, error, and optional body.

    If `keyword` is provided, the response body is read (up to BODY_READ_LIMIT
    bytes) and checked. A 200 response that does not contain the keyword is
    treated as down with a descriptive error.

    Accepts an optional shared session for efficiency at scale.
    Falls back to creating a short-lived session if none provided.
    """
    async def _do_request(s: aiohttp.ClientSession) -> dict:
        try:
            start = time.monotonic()
            resp  = await asyncio.wait_for(
                s.get(url, allow_redirects=True, ssl=False),
                timeout=10
            )
            ms = int((time.monotonic() - start) * 1000)

            # Read body only when a keyword check is needed
            body = None
            if keyword:
                try:
                    raw  = await asyncio.wait_for(
                        resp.content.read(BODY_READ_LIMIT), timeout=5
                    )
                    body = raw.decode("utf-8", errors="replace")
                except Exception:
                    body = ""

            # Determine up/down
            http_up = resp.status < 400

            if http_up and keyword and body is not None:
                found = check_keyword(body, keyword, keyword_case_sensitive)
                if not found:
                    return {
                        "up":          False,
                        "status_code": resp.status,
                        "ms":          ms,
                        "error":       f'Keyword not found: "{keyword}"',
                        "body":        body,
                    }

            return {
                "up":          http_up,
                "status_code": resp.status,
                "ms":          ms,
                "error":       None,
                "body":        body,
            }

        except asyncio.TimeoutError:
            return {"up": False, "status_code": None, "ms": None,
                    "error": "Timeout", "body": None}
        except aiohttp.ClientConnectorError:
            return {"up": False, "status_code": None, "ms": None,
                    "error": "Connection refused", "body": None}
        except Exception as e:
            return {"up": False, "status_code": None, "ms": None,
                    "error": str(e), "body": None}

    if session and not session.closed:
        return await _do_request(session)

    async with aiohttp.ClientSession() as s:
        return await _do_request(s)


def check_keyword(body: str, keyword: str, case_sensitive: bool = False) -> bool:
    """Return True if `keyword` appears in `body`."""
    if case_sensitive:
        return keyword in body
    return keyword.lower() in body.lower()


def check_ssl(hostname: str) -> dict:
    """Check SSL certificate expiry for a hostname."""
    from datetime import datetime
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
            s.settimeout(5)
            s.connect((hostname, 443))
            cert = s.getpeercert()
        expire_str  = cert["notAfter"]
        expire_date = datetime.strptime(expire_str, "%b %d %H:%M:%S %Y %Z")
        days_left   = (expire_date - datetime.now()).days
        return {"valid": True, "days_left": days_left, "expires": expire_str}
    except Exception as e:
        return {"valid": False, "days_left": None, "error": str(e)}


def is_valid_url_format(url: str) -> bool:
    """Check URL has valid scheme, netloc, and TLD."""
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return False
        if not parsed.netloc:
            return False
        if "." not in parsed.netloc:
            return False
        if parsed.netloc in ("localhost", "127.0.0.1"):
            return False
        return True
    except Exception:
        return False


async def verify_url_reachable(url: str) -> dict:
    """
    Real HTTP request to confirm the URL is reachable.
    Used only during /add — not for ongoing monitoring.
    """
    try:
        async with aiohttp.ClientSession() as session:
            resp = await asyncio.wait_for(
                session.get(url, allow_redirects=True, ssl=False),
                timeout=10
            )
            return {"reachable": True, "error": None}
    except asyncio.TimeoutError:
        return {"reachable": False, "error": "Request timed out — is the URL correct?"}
    except aiohttp.ClientConnectorError:
        return {"reachable": False, "error": "Could not connect — URL may not exist."}
    except aiohttp.InvalidURL:
        return {"reachable": False, "error": "Invalid URL format."}
    except Exception as e:
        return {"reachable": False, "error": str(e)}


async def create_shared_session() -> aiohttp.ClientSession:
    """
    Long-lived session stored in bot_data and reused across all monitor checks.
    """
    connector = aiohttp.TCPConnector(
        limit=100,
        limit_per_host=3,
        ttl_dns_cache=300,
    )
    return aiohttp.ClientSession(
        connector=connector,
        timeout=aiohttp.ClientTimeout(total=12),
    )
