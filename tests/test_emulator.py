def test_emulator_init():
    from src.emulator import MobileBrowser
    browser = MobileBrowser()
    assert browser.proxy is None
