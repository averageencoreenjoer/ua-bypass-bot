from loguru import logger
import os
import time
from twocaptcha import TwoCaptcha
from playwright.sync_api import Page


class CaptchaSolver:
    def __init__(self):
        api_key = os.getenv("TWO_CAPTCHA_API_KEY")
        if not api_key:
            logger.warning("2Captcha API key not set, solver will not work")
        self.solver = TwoCaptcha(api_key) if api_key else None

    def is_captcha_html(self, html: str) -> bool:
        text = html.lower()
        needles = [
            "our systems have detected unusual traffic",
            "to continue, please verify",
            "enter the characters you see",
            "captcha",
            "g-recaptcha",
            "recaptcha/api2",
        ]
        return any(n in text for n in needles)

    def solve_recaptcha_v2(self, page: Page, sitekey: str, url: str, timeout=180) -> bool:
        if not self.solver:
            logger.error("2Captcha solver not initialized")
            return False

        try:
            logger.info("Submitting captcha to 2Captcha...")
            result = self.solver.recaptcha(sitekey=sitekey, url=url)
            token = result.get("code")
            if not token:
                logger.error("No captcha token received from 2Captcha")
                return False

            logger.info("Injecting captcha token into page...")
            page.evaluate(
                """token => {
                    document.querySelectorAll('textarea[name="g-recaptcha-response"]').forEach(el => el.value = token);
                }""",
                token
            )
            page.evaluate("""() => {
                let form = document.querySelector('form');
                if (form) form.submit();
            }""")
            time.sleep(3)
            return True
        except Exception as e:
            logger.error(f"2Captcha solving failed: {e}")
            return False
