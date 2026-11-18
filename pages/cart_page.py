"""Page Object Model for the SauceDemo cart page."""

from playwright.sync_api import Page, expect


class CartPage:
    """Page Object for the cart page."""

    def __init__(self, page: Page):
        self.page = page

    def navigate(self) -> None:
        """Navigate to the cart page."""
        self.page.locator('[data-test="shopping-cart-link"]').click()
        self.page.wait_for_url("**/cart.html")

    def get_cart_items(self) -> list:
        """Get all items in the cart as a list of dicts."""
        items = self.page.locator('[data-test="cart-list"] [data-test="inventory-item"]').all()
        result = []
        for item in items:
            name = item.locator('[data-test="inventory-item-name"]').inner_text()
            price = item.locator('[data-test="inventory-item-price"]').inner_text()
            result.append({"name": name, "price": price})
        return result

    def get_item_count(self) -> int:
        """Get the number of items in the cart."""
        items = self.page.locator('[data-test="cart-list"] [data-test="inventory-item"]').all()
        return len(items)

    def click_checkout(self) -> None:
        """Click the Checkout button."""
        self.page.locator('[data-test="checkout"]').click()
        self.page.wait_for_url("**/checkout-step-one.html")

    def click_continue_shopping(self) -> None:
        """Click Continue Shopping to return to inventory."""
        self.page.locator('[data-test="continue-shopping"]').click()
        self.page.wait_for_url("**/inventory.html")

    def expect_item_present(self, product_name: str, price: str) -> None:
        """Assert that a specific item is in the cart with the correct price."""
        items = self.get_cart_items()
        matching = [item for item in items if item["name"] == product_name]
        assert len(matching) == 1, (
            f"Expected 1 '{product_name}' in cart, found {len(matching)}"
        )
        assert matching[0]["price"] == price, (
            f"Expected price {price} for '{product_name}', got {matching[0]['price']}"
        )

    def expect_item_count(self, count: int) -> None:
        """Assert the cart has the expected number of items."""
        actual = self.get_item_count()
        assert actual == count, f"Expected {count} items in cart, found {actual}"