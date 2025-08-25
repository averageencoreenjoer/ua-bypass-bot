import csv
import json
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import requests
from loguru import logger


def setup_logging():
    Path("logs").mkdir(exist_ok=True)
    logger.add("logs/app.log", rotation="1 MB", retention=5, enqueue=True, level="INFO")


def fetch_page(url: str) -> str:
    logger.info(f"Fetching page: {url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A372 "
        "Safari/604.1"
    }
    resp = requests.get(url, headers=headers, timeout=20)
    resp.raise_for_status()
    return resp.text


def load_fixture(filename: str) -> str:
    path = Path("tests/fixtures") / filename
    return path.read_text(encoding="utf-8")


def clean_outbound_url(href: str) -> str:
    if href.startswith("/url?"):
        qs = parse_qs(href.split("?", 1)[1])
        if "q" in qs and qs["q"]:
            return qs["q"][0]
    return href


def save_json(path: Path, data: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info(f"JSON saved to {path}")


def save_csv(path: Path, rows: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        logger.info(f"CSV saved (empty) to {path}")
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    logger.info(f"CSV saved to {path}")
