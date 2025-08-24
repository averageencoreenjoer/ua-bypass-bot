from pathlib import Path
from datetime import datetime
from loguru import logger
from src.emulator import MobileBrowser

RESULTS_HTML = Path("results/html")
RESULTS_IMG = Path("results/screenshots")
RESULTS_HTML.mkdir(parents=True, exist_ok=True)
RESULTS_IMG.mkdir(parents=True, exist_ok=True)


def run_demo():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    browser = MobileBrowser()
    try:
        browser.start()
        url = "https://www.google.com/search?q=test"
        browser.open_url(url)
        html_path = RESULTS_HTML / f"demo_{ts}.html"
        img_path = RESULTS_IMG / f"demo_{ts}.png"
        logger.info(f"Saving HTML to {html_path}")
        html_path.write_text(browser.page.content(), encoding="utf-8")
        logger.info(f"Saving screenshot to {img_path}")
        browser.screenshot(str(img_path))
        logger.success("Demo run completed")
    finally:
        browser.close()


if __name__ == "__main__":
    run_demo()
