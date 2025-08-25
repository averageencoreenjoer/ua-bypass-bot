import pytest
from src.search import parse_top_results, find_link_by_domain


@pytest.fixture
def google_html_fixture():
    return """
    <html>
        <body>
            <div id="search">
                <div class="g">
                    <a href="https://www.example.com/result1"><h3>Первый результат</h3></a>
                    <div>Текст описания 1</div>
                </div>
                <div class="g">
                    <a href="https://www.google.com/some/path"><h3>Второй результат от Google</h3></a>
                    <div>Текст описания 2</div>
                </div>
                <div class="g">
                    <a href="https://www.example.org/another"><h3>Третий результат</h3></a>
                    <div>Текст описания 3</div>
                </div>
            </div>
        </body>
    </html>
    """


def test_parse_top_results(google_html_fixture):
    results = parse_top_results(google_html_fixture, engine="google", limit=3)

    assert len(results) == 3
    assert results[0]['title'] == "Первый результат"
    assert results[0]['url'] == "https://www.example.com/result1"
    assert results[1]['title'] == "Второй результат от Google"
    assert results[1]['url'] == "https://www.google.com/some/path"


def test_parse_top_results_with_limit(google_html_fixture):
    results = parse_top_results(google_html_fixture, engine="google", limit=1)
    assert len(results) == 1
    assert results[0]['title'] == "Первый результат"


def test_find_link_by_domain(google_html_fixture):
    all_results = parse_top_results(google_html_fixture, engine="google")

    matched_results = [r for r in all_results if "example.com" in r['url']]

    assert len(matched_results) == 1
    assert matched_results[0]['url'] == "https://www.example.com/result1"


def test_find_link_by_domain_no_match(google_html_fixture):
    all_results = parse_top_results(google_html_fixture, engine="google")
    matched_results = [r for r in all_results if "nonexistent.com" in r['url']]
    assert len(matched_results) == 0
