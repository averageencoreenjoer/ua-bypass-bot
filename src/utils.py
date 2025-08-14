"""
Helper functions for HTTP requests and parsing.
"""

import requests
from loguru import logger


def fetch_page(url: str) -> str:
    logger.info(f"Fetching page: {url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A372 "
        "Safari/604.1"
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.text
