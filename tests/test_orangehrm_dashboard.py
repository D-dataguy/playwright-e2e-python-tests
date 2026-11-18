import os

from playwright.sync_api import Page, expect


ORANGEHRM_BASE_URL = os.getenv(
    "ORANGEHRM_BASE_URL",
    "https://opensource-demo.orangehrmlive.com",
).rstrip("/")
ORANGEHRM_USERNAME = os.getenv("ORANGEHRM_USERNAME", "Admin")
ORANGEHRM_PASSWORD = os.getenv("ORANGEHRM_PASSWORD", "admin123")


def test_admin_dashboard_displays_core_widgets(page: Page) -> None:
    page.goto(
        f"{ORANGEHRM_BASE_URL}/web/index.php/auth/login",
        wait_until="commit",
    )
    page.get_by_role("textbox", name="Username").fill(ORANGEHRM_USERNAME)
    page.get_by_role("textbox", name="Password").fill(ORANGEHRM_PASSWORD)
    page.get_by_role("button", name="Login").click()

    page.wait_for_url("**/dashboard/index")
    expect(page.get_by_role("heading", name="Dashboard")).to_be_visible()

    for widget_title in (
        "Time at Work",
        "My Actions",
        "Quick Launch",
        "Buzz Latest Posts",
        "Employees on Leave Today",
        "Employee Distribution by Sub Unit",
        "Employee Distribution by Location",
    ):
        expect(page.get_by_text(widget_title, exact=True)).to_be_visible()