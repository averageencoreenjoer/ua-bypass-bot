import time
import requests
from loguru import logger
from .config import ANTICAPTCHA_KEY


class CaptchaSolver:
    def __init__(self, api_key: str = ANTICAPTCHA_KEY):
        if not api_key:
            raise ValueError("ANTICAPTCHA_KEY is not set in .env")
        self.api_key = api_key
        self.in_url = "http://2captcha.com/in.php"
        self.res_url = "http://2captcha.com/res.php"

    def solve_image_captcha(self, image_path: str, timeout: int = 120) -> str:
        """
        Send image captcha to 2Captcha and return the solution text.
        """
        logger.info("Submitting captcha to 2Captcha...")
        with open(image_path, "rb") as img:
            files = {"file": img}
            payload = {"key": self.api_key, "method": "post", "json": 1}
            resp = requests.post(self.in_url, files=files, data=payload).json()

        if resp.get("status") != 1:
            raise RuntimeError(f"Failed to submit captcha: {resp.get('request')}")

        captcha_id = resp["request"]
        logger.info(f"Captcha submitted, ID: {captcha_id}, waiting for solution...")

        start_time = time.time()
        while True:
            time.sleep(5)
            check = requests.get(
                self.res_url, params={"key": self.api_key, "action": "get", "id": captcha_id, "json": 1}
            ).json()

            if check.get("status") == 1:
                solution = check["request"]
                logger.success(f"Captcha solved: {solution}")
                return solution

            if time.time() - start_time > timeout:
                raise TimeoutError("Captcha solving timed out.")

            logger.debug("Waiting for captcha solution...")
