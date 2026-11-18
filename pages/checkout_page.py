"""Page Object Model for the SauceDemo checkout pages."""

from playwright.sync_api import Page, expect


class CheckoutPage:
    """Page Object for checkout pages (Step 1 and Step 2)."""

    def __init__(self, page: Page):
        self.page = page

    def navigate_step_one(self) -> None:
        """Navigate to checkout step 1 (personal info)."""
        self.page.goto("https://www.saucedemo.com/checkout-step-one.html")
        self.page.wait_for_load_state("networkidle")

    def fill_step_one(self, first_name: str, last_name: str, postal_code: str) -> None:
        """Fill out checkout step 1 personal information."""
        self.page.locator('[data-test="firstName"]').fill(first_name)
        self.page.locator('[data-test="lastName"]').fill(last_name)
        self.page.locator('[data-test="postalCode"]').fill(postal_code)

    def continue_checkout(self) -> None:
        """Continue to checkout step 2."""
        self.page.locator('[data-test="continue"]').click()
        self.page.wait_for_load_state("networkidle")

    def complete_purchase(self) -> None:
        """Finish the purchase."""
        self.page.locator('[data-test="finish"]').click()
        self.page.wait_for_url("**/checkout-complete.html")

    def get_order_summary(self) -> dict:
        """Get the order summary information."""
        summary = {
            "subtotal": self.page.locator(".summary_subtotal_label").inner_text(),
            "tax": self.page.locator(".summary_tax_label").inner_text(),
            "total": self.page.locator(".summary_total_label").inner_text(),
        }
        return summary

    def expect_error_containing(self, text: str) -> None:
        """Assert that an error message containing the given text is visible."""
        expect(self.page.locator('[data-test="error"]')).to_contain_text(text)

    def expect_continue_button_present(self) -> None:
        """Assert the Continue button is present."""
        expect(self.page.locator('[data-test="continue"]')).to_be_visible()

    def expect_finish_button_present(self) -> None:
        """Assert the Finish button is present."""
        expect(self.page.locator('[data-test="finish"]')).to_be_visible()

    def expect_order_complete(self) -> None:
        """Assert that the order was completed successfully."""
        expect(self.page.locator('[data-test="complete-header"]')).to_have_text(
            "Thank you for your order!"
        )
        expect(self.page.locator('[data-test="back-to-products"]')).to_be_visible()