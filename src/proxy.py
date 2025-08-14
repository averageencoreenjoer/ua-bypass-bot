"""
Proxy manager with rotation support.
"""

from itertools import cycle
from loguru import logger
from .config import PROXY_LIST_PATH


class ProxyManager:
    def __init__(self):
        with open(PROXY_LIST_PATH, "r") as f:
            proxies = [line.strip() for line in f if line.strip()]
        if not proxies:
            raise ValueError("Proxy list is empty.")
        self.proxy_cycle = cycle(proxies)

    def get_next_proxy(self) -> str:
        proxy = next(self.proxy_cycle)
        logger.info(f"Using proxy: {proxy}")
        return proxy
