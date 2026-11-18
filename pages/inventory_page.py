"""Page Object Model for the SauceDemo inventory page."""

from playwright.sync_api import Page, expect


class InventoryPage:
    """Page Object for the inventory page after login."""

    # Expected products with their prices
    PRODUCTS = [
        ("Sauce Labs Backpack", "$29.99"),
        ("Sauce Labs Bike Light", "$9.99"),
        ("Sauce Labs Bolt T-Shirt", "$15.99"),
        ("Sauce Labs Fleece Jacket", "$49.99"),
        ("Sauce Labs Onesie", "$7.99"),
        ("Test.allTheThings() T-Shirt (Red)", "$15.99"),
    ]

    def __init__(self, page: Page):
        self.page = page

    def add_to_cart(self, product_name: str) -> None:
        """Add a specific product to the cart."""
        slug = product_name.lower().replace(" ", "-").replace("(", "").replace(")", "")
        self.page.locator(f'[data-test="add-to-cart-{slug}"]').click()

    def remove_from_cart(self, product_name: str) -> None:
        """Remove a specific product from the cart."""
        slug = product_name.lower().replace(" ", "-").replace("(", "").replace(")", "")
        self.page.locator(f'[data-test="remove-{slug}"]').click()

    def get_cart_badge_count(self) -> str:
        """Get the cart badge text. Returns empty string if no badge."""
        badge = self.page.locator('[data-test="shopping-cart-badge"]')
        if badge.count() == 0:
            return "0"
        return badge.inner_text()

    def expect_cart_badge(self, count: str) -> None:
        """Assert the cart badge shows the expected count."""
        expect(self.page.locator('[data-test="shopping-cart-badge"]')).to_have_text(count)

    def expect_cart_badge_absent(self) -> None:
        """Assert that the cart badge is not present."""
        expect(self.page.locator('[data-test="shopping-cart-badge"]')).to_have_count(0)

    def go_to_cart(self) -> None:
        """Navigate to the cart page."""
        self.page.locator('[data-test="shopping-cart-link"]').click()
        self.page.wait_for_url("**/cart.html")

    def open_menu(self) -> None:
        """Open the side menu."""
        self.page.locator("#react-burger-menu-btn").click()

    def close_menu(self) -> None:
        """Close the side menu."""
        self.page.locator("#react-burger-cross-btn").click()

    def logout(self) -> None:
        """Log out via the side menu."""
        self.open_menu()
        self.page.locator('[data-test="logout-sidebar-link"]').click()
        self.page.wait_for_url("https://www.saucedemo.com/")

    def reset_app(self) -> None:
        """Reset the app state via the side menu."""
        self.open_menu()
        self.page.locator('[data-test="reset-sidebar-link"]').click()
        self.close_menu()

    def expect_inventory_visible(self) -> None:
        """Assert that the inventory list is visible."""
        expect(self.page.locator(".inventory_list")).to_be_visible()

    def expect_all_products_displayed(self) -> None:
        """Assert that all 6 products are displayed with correct names and prices."""
        self.page.locator(".inventory_item").first.wait_for()
        items = self.page.locator(".inventory_item").all()
        assert len(items) == 6, f"Expected 6 products, found {len(items)}"

        for i, (expected_name, expected_price) in enumerate(self.PRODUCTS):
            item = items[i]
            expect(item.locator(".inventory_item_name")).to_have_text(expected_name)
            expect(item.locator(".inventory_item_price")).to_have_text(expected_price)