"""
Captcha detection and solving with 2captcha API.
"""

import requests
from loguru import logger
from .config import ANTICAPTCHA_KEY


def solve_image_captcha(image_path: str) -> str:
    """
    Send image captcha to 2captcha for solving.
    """
    logger.info("Sending captcha to 2captcha...")
    url = "http://2captcha.com/in.php"
    with open(image_path, "rb") as img:
        files = {"file": img}
        payload = {"key": ANTICAPTCHA_KEY, "method": "post"}
        resp = requests.post(url, data=payload, files=files)
        return resp.text
