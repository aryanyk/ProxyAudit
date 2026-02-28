```markdown
# 🚀 ProxyAudit

**ProxyAudit** is a high-performance, concurrent proxy validation library that scrapes public proxy feeds and filters only the currently working proxies by protocol.

Built for reliability, speed, and clean integration into automation pipelines.

---

## 🔍 What is ProxyAudit?

ProxyAudit:

- Fetches proxy lists from public URLs or APIs  
- Normalizes proxy formats (`protocol://ip:port` or `ip:port`)  
- Validates proxies concurrently  
- Classifies working proxies by protocol  
- Saves validated proxies into structured files  

Perfect for:

- Scraping pipelines  
- Security research  
- Automation workflows  
- Data collection systems  
- Proxy auditing & monitoring  

---

## ⚡ Features

- ✅ Supports `HTTP`, `HTTPS`, `SOCKS4`, `SOCKS5`
- ✅ High concurrency (configurable workers)
- ✅ Async + Sync API support
- ✅ Timeout control
- ✅ Protocol auto-detection
- ✅ File-based output per protocol
- ✅ Notebook-friendly async interface

---

## 📦 Installation

```bash
pip install proxyaudit

```

## 🚀 Quick Start (Synchronous)

```python
from proxyaudit import run_proxy_check

proxy_url = "[https://example.com/proxy-list.txt](https://example.com/proxy-list.txt)"

working = run_proxy_check(
    proxy_url,
    ["http", "https", "socks4", "socks5"]
)

print(working["http"][:5])

```

## ⚡ Async Usage (Recommended for Notebooks / Async Apps)

```python
from proxyaudit import run_proxy_check_async

working = await run_proxy_check_async(
    "[https://example.com/proxy-list.txt](https://example.com/proxy-list.txt)",
    ["http", "https"],
    timeout=8,
    concurrency=200,
)

```

## 🔬 What Gets Validated?

ProxyAudit performs:

* Protocol verification (`http`, `https`, `socks4`, `socks5`)
* Connectivity test against a target URL (default: `http://www.google.com`)
* Timeout-based validation
* Concurrent execution with adjustable worker count

## 📁 Output Files

Successfully validated proxies are saved into:

* `http.txt`
* `https.txt`
* `socks4.txt`
* `socks5.txt`

Each file contains only working proxies for that protocol.

## 🧠 API Reference

### `run_proxy_check(...)`

```python
run_proxy_check(
    proxy_list_url,
    allowed_protocols,
    test_url="[http://www.google.com](http://www.google.com)",
    timeout=5,
    concurrency=100
)

```

**Description:**
Synchronous API for scripts and CLI-style execution.

**Returns:**

```json
{
    "http": [...],
    "https": [...],
    "socks4": [...],
    "socks5": [...]
}

```

### `run_proxy_check_async(...)`

```python
run_proxy_check_async(
    proxy_list_url,
    allowed_protocols,
    test_url="[http://www.google.com](http://www.google.com)",
    timeout=5,
    concurrency=100
)

```

**Description:**
Async API for integration inside existing event loops (FastAPI, Jupyter, asyncio apps).

## ⚙️ Configuration Parameters

| Parameter | Description |
| --- | --- |
| `proxy_list_url` | URL or API endpoint containing proxy list |
| `allowed_protocols` | List of protocols to validate |
| `test_url` | Target URL used for connectivity testing |
| `timeout` | Max seconds before proxy fails |
| `concurrency` | Number of concurrent validation workers |

## 📊 Performance Tuning

For large proxy lists:

* Increase concurrency (200–500 for strong machines)
* Adjust timeout depending on expected latency
* Use async API for best throughput

## 🛡️ Use Cases

* Rotating proxy pool generation
* Proxy health monitoring
* Data scraping infrastructure
* Anonymous traffic routing
* Compliance or network testing tools

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📄 License

MIT License

```

Would you like me to draft up any of those extra sections you mentioned, like the badge-enhanced header, the CLI-ready version, or the benchmark/architecture diagram section to add to this?

```
