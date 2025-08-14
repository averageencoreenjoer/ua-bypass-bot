"""
Mobile browser emulation using Playwright.
"""

from playwright.sync_api import sync_playwright
from loguru import logger


class MobileBrowser:
    def __init__(self, proxy: str | None = None):
        self.proxy = proxy
        self.browser = None
        self.page = None

    def start(self):
        logger.info("Starting mobile browser...")
        playwright = sync_playwright().start()
        device = playwright.devices["iPhone 12"]
        launch_args = {"headless": False}
        if self.proxy:
            launch_args["proxy"] = {"server": self.proxy}

        self.browser = playwright.chromium.launch(**launch_args)
        self.page = self.browser.new_page(**device)

    def open_url(self, url: str):
        if not self.page:
            raise RuntimeError("Browser not started.")
        logger.info(f"Opening URL: {url}")
        self.page.goto(url)

    def screenshot(self, path: str):
        self.page.screenshot(path=path)

    def close(self):
        if self.browser:
            self.browser.close()
