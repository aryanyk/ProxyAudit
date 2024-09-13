# setup.py
from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="proxyaudit",
    version="0.4",
    packages=find_packages(),
    install_requires=[
        "asyncio",
        "aiohttp",
        "urllib3"
        
        ],
    author="Aryan Khandhadiya",
    author_email="aryanyk562@gmail.com",
    description="A package to fetch and check the working HTTP,HTTPS,SOCKS4,SOCKS5 proxies from a list of proxies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aryanyk/proxyaudit",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
