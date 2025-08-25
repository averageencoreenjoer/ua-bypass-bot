import os
from dotenv import load_dotenv

load_dotenv()

ANTICAPTCHA_KEY = os.getenv("ANTICAPTCHA_KEY")
PROXY_LIST_PATH = os.getenv("PROXY_LIST_PATH", "proxies.txt")
TARGET_DOMAIN = os.getenv("TARGET_DOMAIN", "example.com")
TWO_CAPTCHA_API_KEY = os.getenv("TWO_CAPTCHA_API_KEY")
