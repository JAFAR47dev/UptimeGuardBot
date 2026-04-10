#services/checker.py
import aiohttp
import asyncio
import time
import ssl


import aiohttp
import asyncio
import time
from urllib.parse import urlparse

async def check_url(url: str, session: aiohttp.ClientSession = None) -> dict:
    """
    Ping a URL and return status, response time, error.
    Accepts an optional shared session for efficiency at scale.
    Falls back to creating a local session if none is provided.
    """
    async def _do_request(s: aiohttp.ClientSession) -> dict:
        try:
            start = time.monotonic()
            resp  = await asyncio.wait_for(
                s.get(url, allow_redirects=True, ssl=False),
                timeout=10
            )
            ms    = int((time.monotonic() - start) * 1000)
            return {
                "up": resp.status < 400,
                "status_code": resp.status,
                "ms": ms,
                "error": None
            }
        except asyncio.TimeoutError:
            return {"up": False, "status_code": None,
                    "ms": None, "error": "Timeout"}
        except aiohttp.ClientConnectorError:
            return {"up": False, "status_code": None,
                    "ms": None, "error": "Connection refused"}
        except Exception as e:
            return {"up": False, "status_code": None,
                    "ms": None, "error": str(e)}

    if session and not session.closed:
        return await _do_request(session)

    # Fallback — create a short-lived session
    async with aiohttp.ClientSession() as s:
        return await _do_request(s)

       
def check_ssl(hostname: str) -> dict:
    """Check SSL certificate expiry for a hostname."""
    import ssl, socket
    from datetime import datetime
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(
            socket.socket(), server_hostname=hostname
        ) as s:
            s.settimeout(5)
            s.connect((hostname, 443))
            cert = s.getpeercert()
        expire_str = cert["notAfter"]
        expire_date = datetime.strptime(expire_str, "%b %d %H:%M:%S %Y %Z")
        days_left = (expire_date - datetime.now()).days
        return {"valid": True, "days_left": days_left, "expires": expire_str}
    except Exception as e:
        return {"valid": False, "days_left": None, "error": str(e)}
        
from urllib.parse import urlparse

def is_valid_url_format(url: str) -> bool:
    """Check URL has valid scheme, netloc, and TLD."""
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return False
        if not parsed.netloc:
            return False
        # Must have at least one dot in the domain (e.g. google.com)
        if "." not in parsed.netloc:
            return False
        # Reject localhost and raw IPs optionally — remove if you want to allow them
        if parsed.netloc in ("localhost", "127.0.0.1"):
            return False
        return True
    except Exception:
        return False

async def verify_url_reachable(url: str) -> dict:
    """
    Do a real HTTP request to confirm the URL is reachable.
    Returns {"reachable": bool, "error": str|None}
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
    Create a long-lived session to be stored in bot_data
    and reused across all monitor checks.
    Connector limits prevent overwhelming the event loop
    with too many concurrent connections.
    """
    connector = aiohttp.TCPConnector(
        limit=100,          # max concurrent connections total
        limit_per_host=3,   # max concurrent per domain
        ttl_dns_cache=300   # cache DNS results for 5 min
    )
    return aiohttp.ClientSession(
        connector=connector,
        timeout=aiohttp.ClientTimeout(total=12)
    )
    