import os

from playwright.sync_api import Page, expect

SAUCEDEMO_BASE_URL = os.getenv(
    "SAUCEDEMO_BASE_URL", "https://www.saucedemo.com"
).rstrip("/")
SAUCEDEMO_USERNAME = os.getenv("SAUCEDEMO_USERNAME", "standard_user")
SAUCEDEMO_PASSWORD = os.getenv("SAUCEDEMO_PASSWORD", "secret_sauce")


def login(page: Page) -> None:
    """Helper to log in as standard user."""
    page.goto(f"{SAUCEDEMO_BASE_URL}/", wait_until="commit")
    page.get_by_role("textbox", name="Username").fill(SAUCEDEMO_USERNAME)
    page.get_by_role("textbox", name="Password").fill(SAUCEDEMO_PASSWORD)
    page.get_by_role("button", name="Login").click()
    page.wait_for_url("**/inventory.html")
    expect(page.locator(".inventory_list")).to_be_visible()


def test_login_success(page: Page) -> None:
    """Standard user can log in and lands on inventory page."""
    page.goto(f"{SAUCEDEMO_BASE_URL}/", wait_until="commit")
    page.get_by_role("textbox", name="Username").fill(SAUCEDEMO_USERNAME)
    page.get_by_role("textbox", name="Password").fill(SAUCEDEMO_PASSWORD)
    page.get_by_role("button", name="Login").click()

    page.wait_for_url("**/inventory.html")
    expect(page.locator(".inventory_list")).to_be_visible()
    expect(page.locator('[data-test="shopping-cart-link"]')).to_be_visible()


def test_login_locked_out_user_shows_error(page: Page) -> None:
    """Locked out user sees appropriate error message."""
    page.goto(f"{SAUCEDEMO_BASE_URL}/", wait_until="commit")
    page.get_by_role("textbox", name="Username").fill("locked_out_user")
    page.get_by_role("textbox", name="Password").fill(SAUCEDEMO_PASSWORD)
    page.get_by_role("button", name="Login").click()

    expect(page.locator('[data-test="error"]')).to_contain_text(
        "Sorry, this user has been locked out"
    )


def test_inventory_displays_products(page: Page) -> None:
    """Inventory page shows all 6 products with names and prices."""
    login(page)

    items = page.locator(".inventory_item").all()
    assert len(items) == 6

    expected_products = [
        ("Sauce Labs Backpack", "$29.99"),
        ("Sauce Labs Bike Light", "$9.99"),
        ("Sauce Labs Bolt T-Shirt", "$15.99"),
        ("Sauce Labs Fleece Jacket", "$49.99"),
        ("Sauce Labs Onesie", "$7.99"),
        ("Test.allTheThings() T-Shirt (Red)", "$15.99"),
    ]

    for i, (expected_name, expected_price) in enumerate(expected_products):
        item = items[i]
        expect(item.locator(".inventory_item_name")).to_have_text(expected_name)
        expect(item.locator(".inventory_item_price")).to_have_text(expected_price)


def test_add_single_item_to_cart_updates_badge(page: Page) -> None:
    """Adding an item updates the cart badge count."""
    login(page)

    # Add backpack to cart
    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()

    expect(page.locator('[data-test="shopping-cart-badge"]')).to_have_text("1")


def test_add_multiple_items_to_cart(page: Page) -> None:
    """Adding multiple items updates the cart badge accordingly."""
    login(page)

    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()
    page.locator('[data-test="add-to-cart-sauce-labs-bike-light"]').click()
    page.locator('[data-test="add-to-cart-sauce-labs-bolt-t-shirt"]').click()

    expect(page.locator('[data-test="shopping-cart-badge"]')).to_have_text("3")


def test_remove_item_from_inventory_page(page: Page) -> None:
    """Removing an item from inventory page updates badge and button text."""
    login(page)

    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()
    expect(page.locator('[data-test="shopping-cart-badge"]')).to_have_text("1")

    # Remove button appears after adding
    page.locator('[data-test="remove-sauce-labs-backpack"]').click()
    expect(page.locator('[data-test="shopping-cart-badge"]')).to_have_count(0)


def test_cart_page_shows_added_items(page: Page) -> None:
    """Cart page displays the correct items with names and prices."""
    login(page)
    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()
    page.locator('[data-test="add-to-cart-sauce-labs-bike-light"]').click()

    page.locator('[data-test="shopping-cart-link"]').click()
    page.wait_for_url("**/cart.html")

    # Cart items are inside the cart list container
    cart_items = page.locator(
        '[data-test="cart-list"] [data-test="inventory-item"]'
    ).all()
    assert len(cart_items) == 2

    expect(cart_items[0].locator('[data-test="inventory-item-name"]')).to_have_text(
        "Sauce Labs Backpack"
    )
    expect(cart_items[0].locator('[data-test="inventory-item-price"]')).to_have_text(
        "$29.99"
    )
    expect(cart_items[1].locator('[data-test="inventory-item-name"]')).to_have_text(
        "Sauce Labs Bike Light"
    )
    expect(cart_items[1].locator('[data-test="inventory-item-price"]')).to_have_text(
        "$9.99"
    )


def test_continue_shopping_returns_to_inventory(page: Page) -> None:
    """Continue Shopping button returns user to inventory page."""
    login(page)
    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()
    page.locator('[data-test="shopping-cart-link"]').click()
    page.wait_for_url("**/cart.html")

    page.locator('[data-test="continue-shopping"]').click()
    page.wait_for_url("**/inventory.html")
    expect(page.locator(".inventory_list")).to_be_visible()


def test_checkout_step_one_form_validation(page: Page) -> None:
    """Checkout step one requires all fields to proceed."""
    login(page)
    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()
    page.locator('[data-test="shopping-cart-link"]').click()
    page.wait_for_url("**/cart.html")

    page.locator('[data-test="checkout"]').click()
    page.wait_for_url("**/checkout-step-one.html")

    # Try to continue without filling fields
    page.locator('[data-test="continue"]').click()
    expect(page.locator('[data-test="error"]')).to_contain_text(
        "First Name is required"
    )


def test_checkout_complete_flow(page: Page) -> None:
    """Complete checkout flow from cart to confirmation."""
    login(page)
    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()
    page.locator('[data-test="shopping-cart-link"]').click()
    page.wait_for_url("**/cart.html")

    page.locator('[data-test="checkout"]').click()
    page.wait_for_url("**/checkout-step-one.html")

    # Fill checkout info
    page.locator('[data-test="firstName"]').fill("John")
    page.locator('[data-test="lastName"]').fill("Doe")
    page.locator('[data-test="postalCode"]').fill("12345")
    page.locator('[data-test="continue"]').click()

    page.wait_for_url("**/checkout-step-two.html")
    expect(page.locator('[data-test="finish"]')).to_be_visible()

    # Verify order summary
    expect(page.locator(".summary_subtotal_label")).to_contain_text("29.99")
    expect(page.locator(".summary_tax_label")).to_be_visible()
    expect(page.locator(".summary_total_label")).to_be_visible()

    # Complete purchase
    page.locator('[data-test="finish"]').click()
    page.wait_for_url("**/checkout-complete.html")

    expect(page.locator('[data-test="complete-header"]')).to_have_text(
        "Thank you for your order!"
    )
    expect(page.locator('[data-test="back-to-products"]')).to_be_visible()


def test_menu_logout(page: Page) -> None:
    """User can log out via the side menu."""
    login(page)

    page.locator("#react-burger-menu-btn").click()
    page.locator('[data-test="logout-sidebar-link"]').click()

    page.wait_for_url(f"{SAUCEDEMO_BASE_URL}/")
    expect(page.get_by_role("button", name="Login")).to_be_visible()


def test_menu_reset_app_state(page: Page) -> None:
    """Reset App State clears the cart."""
    login(page)
    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()
    page.locator('[data-test="add-to-cart-sauce-labs-bike-light"]').click()
    expect(page.locator('[data-test="shopping-cart-badge"]')).to_have_text("2")

    page.locator("#react-burger-menu-btn").click()
    page.locator('[data-test="reset-sidebar-link"]').click()
    page.locator("#react-burger-cross-btn").click()

    expect(page.locator('[data-test="shopping-cart-badge"]')).to_have_count(0)


def test_menu_about_link(page: Page) -> None:
    """About link in menu opens Sauce Labs website in new tab."""
    login(page)

    page.locator("#react-burger-menu-btn").click()
    # About link opens in new tab - we can verify it exists
    expect(page.locator('[data-test="about-sidebar-link"]')).to_be_visible()
    expect(page.locator('[data-test="about-sidebar-link"]')).to_have_attribute(
        "href", "https://saucelabs.com/"
    )
