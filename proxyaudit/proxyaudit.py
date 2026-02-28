import asyncio
import socket
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

# Default timeout settings for checking proxies
TIMEOUT = 5
DEFAULT_TEST_URL = "http://www.google.com"

# Output files for different proxy types
HTTP_FILE = "http.txt"
HTTPS_FILE = "https.txt"
SOCKS4_FILE = "socks4.txt"
SOCKS5_FILE = "socks5.txt"

SUPPORTED_PROTOCOLS = {"http", "https", "socks4", "socks5"}


def _get_aiohttp():
    """Import aiohttp lazily so package import does not fail without optional deps."""
    try:
        import aiohttp  # type: ignore
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "proxyaudit requires 'aiohttp' to run proxy checks. "
            "Install it with: pip install aiohttp"
        ) from exc

    try:
        import urllib3

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    except ModuleNotFoundError:
        pass

    return aiohttp


def _normalize_protocols(allowed_protocols: Sequence[str]) -> Set[str]:
    protocols = {protocol.lower().strip() for protocol in allowed_protocols}
    invalid = protocols - SUPPORTED_PROTOCOLS
    if invalid:
        raise ValueError(
            f"Unsupported protocols: {sorted(invalid)}. "
            f"Supported values: {sorted(SUPPORTED_PROTOCOLS)}"
        )
    return protocols


def _expand_proxy_candidates(proxy: str, allowed_protocols: Set[str]) -> List[str]:
    proxy = proxy.strip()
    if not proxy:
        return []

    if "://" in proxy:
        protocol, _ = proxy.split("://", 1)
        protocol = protocol.lower().strip()
        if protocol in allowed_protocols:
            return [proxy]
        return []

    # If protocol is missing (common proxy-list format), test all allowed protocols.
    return [f"{protocol}://{proxy}" for protocol in sorted(allowed_protocols)]


async def fetch_proxies(proxy_list_url: str, session) -> List[str]:
    """Fetch the proxy list asynchronously."""
    async with session.get(proxy_list_url) as response:
        response.raise_for_status()
        proxies_text = await response.text()
        return [line.strip() for line in proxies_text.splitlines() if line.strip()]


async def check_proxy(
    proxy: str,
    allowed_protocols: Set[str],
    session,
    test_url: str,
    timeout: int,
    semaphore: asyncio.Semaphore,
) -> Optional[Tuple[str, str]]:
    """Check if a proxy is working and return its type if it matches allowed protocols."""
    aiohttp = _get_aiohttp()
    for proxy_candidate in _expand_proxy_candidates(proxy, allowed_protocols):
        protocol, ip_port = proxy_candidate.split("://", 1)
        try:
            ip, port = ip_port.split(":")
            int(port)
            socket.inet_aton(ip)
        except (ValueError, OSError):
            continue

        async with semaphore:
            try:
                async with session.get(
                    test_url,
                    proxy=proxy_candidate,
                    timeout=timeout,
                    ssl=False,
                ) as response:
                    if response.status == 200:
                        return protocol, proxy_candidate
            except (aiohttp.ClientError, asyncio.TimeoutError, socket.timeout, ValueError):
                continue

    return None


def save_proxies(working_proxies: Iterable[Tuple[str, str]], allowed_protocols: Set[str]) -> Dict[str, List[str]]:
    """Save working proxies to protocol-specific files and return grouped results."""
    grouped: Dict[str, List[str]] = {protocol: [] for protocol in SUPPORTED_PROTOCOLS}
    for protocol, proxy in working_proxies:
        grouped[protocol].append(proxy)

    if "http" in allowed_protocols:
        with open(HTTP_FILE, "w", encoding="utf-8") as http_file:
            http_file.write("\n".join(grouped["http"]))
            if grouped["http"]:
                http_file.write("\n")

    if "https" in allowed_protocols:
        with open(HTTPS_FILE, "w", encoding="utf-8") as https_file:
            https_file.write("\n".join(grouped["https"]))
            if grouped["https"]:
                https_file.write("\n")

    if "socks4" in allowed_protocols:
        with open(SOCKS4_FILE, "w", encoding="utf-8") as socks4_file:
            socks4_file.write("\n".join(grouped["socks4"]))
            if grouped["socks4"]:
                socks4_file.write("\n")

    if "socks5" in allowed_protocols:
        with open(SOCKS5_FILE, "w", encoding="utf-8") as socks5_file:
            socks5_file.write("\n".join(grouped["socks5"]))
            if grouped["socks5"]:
                socks5_file.write("\n")

    return {protocol: grouped[protocol] for protocol in allowed_protocols}


async def run_proxy_check_async(
    proxy_list_url: str,
    allowed_protocols: Sequence[str],
    test_url: str = DEFAULT_TEST_URL,
    timeout: int = TIMEOUT,
    concurrency: int = 100,
) -> Dict[str, List[str]]:
    """Run proxy checks asynchronously and persist working proxies to files."""
    aiohttp = _get_aiohttp()
    allowed = _normalize_protocols(allowed_protocols)
    semaphore = asyncio.Semaphore(concurrency)

    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        proxies = await fetch_proxies(proxy_list_url, session)
        tasks = [
            check_proxy(proxy, allowed, session, test_url, timeout, semaphore)
            for proxy in proxies
        ]
        results = await asyncio.gather(*tasks)

    working_proxies = [result for result in results if result]
    return save_proxies(working_proxies, allowed)


def run_proxy_check(
    proxy_list_url: str,
    allowed_protocols: Sequence[str],
    test_url: str = DEFAULT_TEST_URL,
    timeout: int = TIMEOUT,
    concurrency: int = 100,
) -> Dict[str, List[str]]:
    """Run the proxy check for the specified protocols from synchronous code."""
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(
            run_proxy_check_async(
                proxy_list_url,
                allowed_protocols,
                test_url=test_url,
                timeout=timeout,
                concurrency=concurrency,
            )
        )

    raise RuntimeError(
        "run_proxy_check() cannot be called from an active event loop. "
        "Use: await run_proxy_check_async(...)"
    )
