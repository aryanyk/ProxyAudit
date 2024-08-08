# proxy_checker.py

import asyncio
import aiohttp
import urllib3
import socket

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Timeout settings for checking proxies
TIMEOUT = 5

# Output files
HTTP_FILE = "proxies.txt"

async def fetch_proxies(proxy_list_url):
    """Fetch the proxy list asynchronously."""
    async with aiohttp.ClientSession() as session:
        async with session.get(proxy_list_url) as response:
            proxies_text = await response.text()
            return proxies_text.splitlines()

async def check_proxy(proxy):
    """Check if a proxy is working."""
    protocol, ip_port = proxy.split("://")
    ip, port = ip_port.split(":")

    # Skip if protocol is https, socks4, or socks5
    if protocol in ["https", "socks4", "socks5"]:
        return None

    proxy_url = f"{protocol}://{ip}:{port}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://www.google.com", proxy=proxy_url, timeout=TIMEOUT, ssl=False) as response:
                if response.status == 200:
                    return protocol, proxy_url
    except (aiohttp.ClientError, asyncio.TimeoutError, socket.timeout):
        return None

def save_proxies(working_proxies):
    """Save working HTTP proxies to a file."""
    with open(HTTP_FILE, "w") as http_file:
        for protocol, proxy in working_proxies:
            http_file.write(proxy + "\n")

async def main(proxy_list_url):
    proxies = await fetch_proxies(proxy_list_url)

    working_proxies = []
    tasks = []
    for proxy in proxies:
        tasks.append(check_proxy(proxy))

    results = await asyncio.gather(*tasks)
    working_proxies = [result for result in results if result]

    save_proxies(working_proxies)

def run_proxy_check(proxy_list_url):
    asyncio.run(main(proxy_list_url))
