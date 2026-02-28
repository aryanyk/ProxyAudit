Open-source library for scraping public proxies and validating only the currently working ones.

`proxyaudit` fetches proxies from a URL/API, tests them concurrently, and stores working proxies by protocol.

## Install

```bash
pip install proxyaudit
```

## Quick start

```python
from proxyaudit import run_proxy_check

proxy_url = "https://example.com/proxy-list.txt"
working = run_proxy_check(proxy_url, ["http", "https", "socks4", "socks5"])
print(working["http"][:5])
```

## Async usage (for notebooks / async apps)

```python
from proxyaudit import run_proxy_check_async

working = await run_proxy_check_async(
    "https://example.com/proxy-list.txt",
    ["http", "https"],
    timeout=8,
    concurrency=200,
)
```

## What is validated

- Supports `http`, `https`, `socks4`, `socks5`.
- Accepts either `protocol://ip:port` or plain `ip:port` input from proxy feeds.
- Tests proxies against a target URL (default: `http://www.google.com`).
- Saves successful proxies into:
  - `http.txt`
  - `https.txt`
  - `socks4.txt`
  - `socks5.txt`

## API

### `run_proxy_check(proxy_list_url, allowed_protocols, test_url="http://www.google.com", timeout=5, concurrency=100)`

Synchronous API for scripts. Returns a dictionary keyed by protocol with working proxies.

### `run_proxy_check_async(proxy_list_url, allowed_protocols, test_url="http://www.google.com", timeout=5, concurrency=100)`

Async API for running inside an existing event loop.
