"""Page Object Model for the SauceDemo login page."""

from playwright.sync_api import Page, expect

from config.settings import SAUCEDEMO_BASE_URL, SAUCEDEMO_PASSWORD, SAUCEDEMO_USERNAME


class LoginPage:
    """Page Object for https://www.saucedemo.com/"""

    def __init__(self, page: Page):
        self.page = page

    def navigate(self) -> None:
        """Navigate to the login page."""
        self.page.goto(f"{SAUCEDEMO_BASE_URL}/", wait_until="commit")

    def enter_username(self, username: str = SAUCEDEMO_USERNAME) -> None:
        """Enter username in the username field."""
        self.page.get_by_role("textbox", name="Username").fill(username)

    def enter_password(self, password: str = SAUCEDEMO_PASSWORD) -> None:
        """Enter password in the password field."""
        self.page.get_by_role("textbox", name="Password").fill(password)

    def click_login(self) -> None:
        """Click the Login button."""
        self.page.get_by_role("button", name="Login").click()

    def login(self, username: str = SAUCEDEMO_USERNAME, password: str = SAUCEDEMO_PASSWORD) -> None:
        """Perform a complete login flow."""
        self.navigate()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        self.page.wait_for_url("**/inventory.html")

    def get_error_message(self) -> str:
        """Get the error message text if present."""
        return self.page.locator('[data-test="error"]').inner_text()

    def expect_error_containing(self, text: str) -> None:
        """Assert that an error message containing the given text is visible."""
        expect(self.page.locator('[data-test="error"]')).to_contain_text(text)

    def expect_login_button_visible(self) -> None:
        """Assert that the Login button is visible."""
        expect(self.page.get_by_role("button", name="Login")).to_be_visible()