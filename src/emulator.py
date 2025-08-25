import random
import time
from playwright.sync_api import sync_playwright
from loguru import logger


class MobileBrowser:
    def __init__(self, proxy: str | None = None, headless: bool = False):
        self.proxy = proxy
        self.browser = None
        self.page = None
        self._playwright = None
        self._headless = headless

    def start(self):
        logger.info("Starting mobile browser...")
        self._playwright = sync_playwright().start()
        device = self._playwright.devices["iPhone 12"]

        launch_args = {"headless": self._headless}
        if self.proxy:
            launch_args["proxy"] = {"server": self.proxy}

        self.browser = self._playwright.chromium.launch(**launch_args)
        self.page = self.browser.new_page(**device)

    def open_url(self, url: str):
        if not self.page:
            raise RuntimeError("Browser not started.")
        logger.info(f"Opening URL: {url}")
        self.page.goto(url, wait_until="domcontentloaded")

    def human_tap(self, selector: str, timeout: int = 5000):
        self.page.wait_for_selector(selector, timeout=timeout)
        box = self.page.locator(selector).bounding_box()
        if box:
            x = box["x"] + box["width"] * random.uniform(0.2, 0.8)
            y = box["y"] + box["height"] * random.uniform(0.2, 0.8)
            self.page.mouse.move(x, y)
            time.sleep(random.uniform(0.05, 0.2))
            self.page.mouse.down()
            time.sleep(random.uniform(0.05, 0.15))
            self.page.mouse.up()
        else:
            self.page.locator(selector).click()

    def human_scroll(self, total_px: int = 2000, step_px: int = 200):
        scrolled = 0
        while scrolled < total_px:
            delta = int(step_px * random.uniform(0.7, 1.3))
            self.page.mouse.wheel(0, delta)
            scrolled += delta
            time.sleep(random.uniform(0.2, 0.5))

    def screenshot(self, path: str):
        self.page.screenshot(path=path, full_page=True)

    def close(self):
        if self.browser:
            self.browser.close()
        if self._playwright:
            self._playwright.stop()
