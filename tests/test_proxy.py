import pytest
from pathlib import Path
from src.proxy import ProxyManager


@pytest.fixture
def proxy_file(tmp_path: Path) -> Path:
    proxies = [
        "http://user1:pass1@proxy1.com:8080",
        "http://user2:pass2@proxy2.com:8080",
        "http://user3:pass3@proxy3.com:8080",
    ]
    p_file = tmp_path / "proxies.txt"
    p_file.write_text("\n".join(proxies))
    return p_file


def test_proxy_manager_loads_proxies(proxy_file, monkeypatch):
    monkeypatch.setattr("src.proxy.PROXY_LIST_PATH", proxy_file)

    manager = ProxyManager()
    assert manager.get_next_proxy() == "http://user1:pass1@proxy1.com:8080"
    assert manager.get_next_proxy() == "http://user2:pass2@proxy2.com:8080"


def test_get_next_proxy_cycles(proxy_file, monkeypatch):
    monkeypatch.setattr("src.proxy.PROXY_LIST_PATH", proxy_file)
    manager = ProxyManager()

    proxy1 = manager.get_next_proxy()
    proxy2 = manager.get_next_proxy()
    proxy3 = manager.get_next_proxy()
    proxy4_should_be_proxy1 = manager.get_next_proxy()

    assert proxy1 == "http://user1:pass1@proxy1.com:8080"
    assert proxy3 == "http://user3:pass3@proxy3.com:8080"
    assert proxy4_should_be_proxy1 == proxy1


def test_proxy_manager_with_empty_file(tmp_path: Path, monkeypatch):
    empty_file = tmp_path / "empty.txt"
    empty_file.touch()

    monkeypatch.setattr("src.proxy.PROXY_LIST_PATH", empty_file)

    with pytest.raises(ValueError, match="Proxy list is empty"):
        ProxyManager()
