import asyncio
import aiohttp
import urllib3
import socket

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Timeout settings for checking proxies
TIMEOUT = 5

# Output files for different proxy types
HTTP_FILE = "http.txt"
HTTPS_FILE = "https.txt"
SOCKS4_FILE = "socks4.txt"
SOCKS5_FILE = "socks5.txt"

async def fetch_proxies(proxy_list_url):
    """Fetch the proxy list asynchronously."""
    async with aiohttp.ClientSession() as session:
        async with session.get(proxy_list_url) as response:
            proxies_text = await response.text()
            return proxies_text.splitlines()

async def check_proxy(proxy, allowed_protocols):
    """Check if a proxy is working and return its type if it matches the allowed protocols."""
    try:
        protocol, ip_port = proxy.split("://")
        ip, port = ip_port.split(":")

        # Check if the protocol is in the allowed protocols
        if protocol not in allowed_protocols:
            return None

        proxy_url = f"{protocol}://{ip}:{port}"

        async with aiohttp.ClientSession() as session:
            async with session.get("http://www.google.com", proxy=proxy_url, timeout=TIMEOUT, ssl=False) as response:
                if response.status == 200:
                    return protocol, proxy_url
    except (aiohttp.ClientError, asyncio.TimeoutError, socket.timeout, ValueError):
        return None

def save_proxies(working_proxies, allowed_protocols):
    """Save working proxies to their respective files based on protocol."""
    if "http" in allowed_protocols:
        with open(HTTP_FILE, "w") as http_file:
            for protocol, proxy in working_proxies:
                if protocol == "http":
                    http_file.write(proxy + "\n")
    
    if "https" in allowed_protocols:
        with open(HTTPS_FILE, "w") as https_file:
            for protocol, proxy in working_proxies:
                if protocol == "https":
                    https_file.write(proxy + "\n")
    
    if "socks4" in allowed_protocols:
        with open(SOCKS4_FILE, "w") as socks4_file:
            for protocol, proxy in working_proxies:
                if protocol == "socks4":
                    socks4_file.write(proxy + "\n")
    
    if "socks5" in allowed_protocols:
        with open(SOCKS5_FILE, "w") as socks5_file:
            for protocol, proxy in working_proxies:
                if protocol == "socks5":
                    socks5_file.write(proxy + "\n")

async def main(proxy_list_url, allowed_protocols):
    proxies = await fetch_proxies(proxy_list_url)

    tasks = [check_proxy(proxy, allowed_protocols) for proxy in proxies]
    results = await asyncio.gather(*tasks)

    working_proxies = [result for result in results if result]
    save_proxies(working_proxies, allowed_protocols)

def run_proxy_check(proxy_list_url, allowed_protocols):
    """Run the proxy check for only the specified allowed protocols."""
    asyncio.run(main(proxy_list_url, allowed_protocols))