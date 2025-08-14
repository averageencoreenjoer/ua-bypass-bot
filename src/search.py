"""
Search engine querying and parsing results.
"""

from loguru import logger
from bs4 import BeautifulSoup
from .utils import fetch_page


def search_query(engine: str, keyword: str, target_domain: str) -> list[dict]:
    """
    Perform a search and return top results.
    """
    if engine.lower() == "google":
        url = f"https://www.google.com/search?q={keyword}"
    elif engine.lower() == "yandex":
        url = f"https://yandex.ru/search/?text={keyword}"
    else:
        raise ValueError("Unsupported search engine")

    html = fetch_page(url)
    soup = BeautifulSoup(html, "html.parser")
    results = []

    for link in soup.select("a"):
        href = link.get("href", "")
        if target_domain in href:
            results.append({"title": link.text, "url": href})

    logger.info(f"Found {len(results)} matching results")
    return results
