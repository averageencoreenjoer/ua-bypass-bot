import pytest
from unittest.mock import patch, MagicMock
from src.emulator import MobileBrowser


@pytest.fixture
def mock_playwright_chain():
    with patch('src.emulator.sync_playwright') as mock_sync_playwright:
        mock_playwright_manager = MagicMock()
        mock_playwright_instance = MagicMock()
        mock_browser = MagicMock()
        mock_page = MagicMock()

        mock_sync_playwright.return_value = mock_playwright_manager
        mock_playwright_manager.start.return_value = mock_playwright_instance

        mock_playwright_instance.devices = {"iPhone 12": {"user_agent": "test-agent"}}

        mock_playwright_instance.chromium.launch.return_value = mock_browser

        mock_browser.new_page.return_value = mock_page

        yield mock_playwright_instance


def test_browser_start_and_close(mock_playwright_chain):
    browser = MobileBrowser(headless=True, proxy="http://proxy:1234")
    browser.start()

    mock_playwright_chain.chromium.launch.assert_called_once_with(
        headless=True,
        proxy={'server': 'http://proxy:1234'}
    )
    mock_playwright_chain.chromium.launch.return_value.new_page.assert_called_once_with(
        **mock_playwright_chain.devices["iPhone 12"]
    )

    browser.close()
    mock_playwright_chain.chromium.launch.return_value.close.assert_called_once()
    mock_playwright_chain.stop.assert_called_once()


def test_browser_open_url(mock_playwright_chain):
    browser = MobileBrowser()
    browser.start()

    mock_page = mock_playwright_chain.chromium.launch.return_value.new_page.return_value

    target_url = "https://www.google.com"
    browser.open_url(target_url)

    mock_page.goto.assert_called_once_with(target_url, wait_until="domcontentloaded")


def test_browser_screenshot(mock_playwright_chain, tmp_path):
    browser = MobileBrowser()
    browser.start()

    mock_page = mock_playwright_chain.chromium.launch.return_value.new_page.return_value

    screenshot_path = str(tmp_path / "screenshot.png")
    browser.screenshot(screenshot_path)

    mock_page.screenshot.assert_called_once_with(path=screenshot_path, full_page=True)
