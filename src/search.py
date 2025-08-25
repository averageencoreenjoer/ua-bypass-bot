from urllib.parse import urlparse
from bs4 import BeautifulSoup
from loguru import logger
from .utils import fetch_page, clean_outbound_url


def search_query(engine: str, keyword: str) -> str:
    if engine.lower() == "google":
        url = f"https://www.google.com/search?q={keyword}&hl=en"
    elif engine.lower() == "yandex":
        url = f"https://yandex.ru/search/?text={keyword}"
    else:
        raise ValueError("Unsupported search engine")
    return fetch_page(url)


def parse_top_results(html: str, engine: str, limit: int = 10) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    results: list[dict] = []

    if engine.lower() == "google":
        for a in soup.select("a:has(h3)")[: limit * 2]:
            href = a.get("href", "")
            title_el = a.select_one("h3")
            if not href or not title_el:
                continue
            url = clean_outbound_url(href)
            if not url.startswith("http"):
                continue
            results.append({"title": title_el.get_text(strip=True), "url": url})
            if len(results) >= limit:
                break

    elif engine.lower() == "yandex":
        for a in soup.select("a[href^='http']")[: limit * 3]:
            title = a.get_text(strip=True)
            if not title:
                continue
            results.append({"title": title, "url": a["href"]})
            if len(results) >= limit:
                break
    else:
        raise ValueError("Unsupported search engine")

    logger.info(f"Parsed {len(results)} organic results ({engine})")
    return results


def search_query_from_html(html: str, target_domain: str, engine: str = "google") -> list[dict]:
    all_results = parse_top_results(html, engine=engine, limit=10)
    filtered = [r for r in all_results if target_domain.lower() in r["url"].lower()]
    logger.info(f"Found {len(filtered)} results matching domain '{target_domain}'")
    return filtered


def find_link_by_domain(results: list[dict], domain_keyword: str) -> dict | None:
    for r in results:
        netloc = urlparse(r["url"]).netloc
        if domain_keyword.lower() in netloc.lower():
            return r
    return None
