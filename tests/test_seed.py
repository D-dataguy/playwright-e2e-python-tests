from playwright.sync_api import Page


def test_seed(page: Page) -> None:
    assert page.url == "about:blank"
