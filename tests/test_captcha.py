import pytest
from unittest.mock import patch, MagicMock
from src.captcha import CaptchaSolver


def test_is_captcha_html():
    solver = CaptchaSolver()
    captcha_html = '<html><body><iframe src="https://www.google.com/recaptcha/api2/anchor"></iframe></body></html>'
    no_captcha_html = '<html><body><h1>Search Results</h1></body></html>'

    assert solver.is_captcha_html(captcha_html) is True
    assert solver.is_captcha_html(no_captcha_html) is False


@patch('src.captcha.TwoCaptcha')
def test_solve_recaptcha_v2_success(mock_twocaptcha, monkeypatch):
    monkeypatch.setenv("TWO_CAPTCHA_API_KEY", "dummy-key")

    mock_solver_instance = MagicMock()
    mock_solver_instance.recaptcha.return_value = {"code": "solved-token"}
    mock_twocaptcha.return_value = mock_solver_instance

    solver = CaptchaSolver()

    mock_page = MagicMock()

    result = solver.solve_recaptcha_v2(mock_page, "some-sitekey", "http://example.com")

    assert result is True
    mock_solver_instance.recaptcha.assert_called_once_with(sitekey="some-sitekey", url="http://example.com")
    assert mock_page.evaluate.call_count == 2


def test_solver_initialization_without_api_key(monkeypatch):
    monkeypatch.delenv("TWO_CAPTCHA_API_KEY", raising=False)

    solver = CaptchaSolver()
    assert solver.solver is None

    assert solver.solve_recaptcha_v2(MagicMock(), "", "") is False
