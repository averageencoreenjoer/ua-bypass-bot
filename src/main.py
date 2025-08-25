import argparse
from pathlib import Path
from datetime import datetime
from loguru import logger

from src.config import TARGET_DOMAIN, PROXY_LIST_PATH
from src.utils import load_fixture, save_json, save_csv, setup_logging
from src.search import parse_top_results, search_query_from_html, find_link_by_domain
from src.captcha import CaptchaSolver
from src.proxy import ProxyManager
from src.emulator import MobileBrowser

RESULTS_HTML = Path("results/html")
RESULTS_IMG = Path("results/screenshots")
RESULTS_DATA = Path("results/data")
for p in (RESULTS_HTML, RESULTS_IMG, RESULTS_DATA):
    p.mkdir(parents=True, exist_ok=True)


def accept_google_consent(browser: MobileBrowser):
    selectors = [
        "text='Accept all'",
        "text='I agree'",
        "text='Agree to all'",
        "button:has-text('Accept all')",
        "button:has-text('I agree')",
        "#L2AGLb",
    ]
    for sel in selectors:
        try:
            browser.human_tap(sel, timeout=1500)
            logger.info("Clicked Google consent")
            return True
        except Exception:
            continue
    logger.info("No consent dialog found")
    return False


def run_fixture(engine: str, keyword: str, target_domain: str):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    html = load_fixture("google_sample.html")
    html_path = RESULTS_HTML / f"fixture_{ts}.html"
    html_path.write_text(html, encoding="utf-8")
    logger.info(f"Fixture HTML saved: {html_path}")

    top10 = parse_top_results(html, engine=engine, limit=10)
    matched = [r for r in top10 if target_domain.lower() in r["url"].lower()]

    json_path = RESULTS_DATA / f"fixture_{ts}.json"
    csv_path = RESULTS_DATA / f"fixture_{ts}.csv"
    save_json(json_path, top10)
    save_csv(csv_path, top10)

    for r in matched:
        logger.info(f"[MATCH] {r['title']} -> {r['url']}")

    logger.success("Fixture run complete.")


def run_live(engine: str, keyword: str, target_domain: str, headless: bool, use_proxy: bool, max_attempts: int = 3):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    solver = CaptchaSolver()
    proxy_iter = None
    proxy = None

    if use_proxy:
        try:
            proxy_iter = ProxyManager()
        except Exception as e:
            logger.warning(f"ProxyManager init failed: {e}")

    attempt = 0
    while attempt < max_attempts:
        attempt += 1
        if proxy_iter:
            proxy = proxy_iter.get_next_proxy()
            logger.info(f"[Attempt {attempt}/{max_attempts}] Using proxy: {proxy}")
        else:
            logger.info(f"[Attempt {attempt}/{max_attempts}] No proxy")

        browser = MobileBrowser(proxy=proxy, headless=headless)
        try:
            browser.start()

            browser.open_url("https://www.google.com/ncr?hl=en")
            accept_google_consent(browser)

            search_url = f"https://www.google.com/search?q={keyword}&hl=en"
            browser.open_url(search_url)
            browser.human_scroll(total_px=1500)

            html = browser.page.content()

            if solver.is_captcha_html(html):
                html_path = RESULTS_HTML / f"live_captcha_{ts}_try{attempt}.html"
                html_path.write_text(html, encoding="utf-8")
                logger.warning(f"Anti-bot page saved: {html_path}")

                if solver.api_key:
                    try:
                        solved = solver.solve_recaptcha(html, url=search_url)
                        if solved:
                            logger.success("CAPTCHA solved via 2captcha")
                            continue
                    except Exception as e:
                        logger.error(f"CAPTCHA solve failed: {e}")

                continue

            html_path = RESULTS_HTML / f"live_{ts}.html"
            img_path = RESULTS_IMG / f"live_{ts}.png"
            html_path.write_text(html, encoding="utf-8")
            browser.screenshot(str(img_path))
            logger.info(f"HTML saved: {html_path}")
            logger.info(f"Screenshot saved: {img_path}")

            top10 = parse_top_results(html, engine=engine, limit=10)
            json_path = RESULTS_DATA / f"live_{ts}.json"
            csv_path = RESULTS_DATA / f"live_{ts}.csv"
            save_json(json_path, top10)
            save_csv(csv_path, top10)

            matched = [r for r in top10 if target_domain.lower() in r["url"].lower()]
            for r in matched:
                logger.info(f"[MATCH] {r['title']} -> {r['url']}")

            logger.success("Live run complete.")
            return

        except Exception as e:
            logger.exception(f"Live run failed on attempt {attempt}: {e}")
        finally:
            browser.close()

    logger.error("Live run aborted after max attempts (likely due to anti-bot/CAPTCHA).")


def build_parser():
    p = argparse.ArgumentParser(description="UA Bypass Bot (fixture/live)")
    p.add_argument("--mode", choices=["fixture", "live"], default="fixture")
    p.add_argument("--engine", choices=["google", "yandex"], default="google")
    p.add_argument("--keyword", default="test")
    p.add_argument("--target-domain", default=TARGET_DOMAIN or "example.com")
    p.add_argument("--headless", action="store_true", help="Run browser headless (live mode)")
    p.add_argument("--use-proxy", action="store_true", help="Enable proxy rotation in live mode")
    return p


def main():
    setup_logging()
    args = build_parser().parse_args()
    logger.info(f"Args: {args}")

    if args.mode == "fixture":
        run_fixture(args.engine, args.keyword, args.target_domain)
    else:
        run_live(args.engine, args.keyword, args.target_domain,
                 headless=args.headless, use_proxy=args.use_proxy)


if __name__ == "__main__":
    main()
