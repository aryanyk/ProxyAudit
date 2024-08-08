# setup.py
from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="proxyaudit",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    author="Aryan Khandhadiya",
    author_email="aryanyk562@gmail.com",
    description="A package to fetch and check the working HTTP proxies from a list of proxies",
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
