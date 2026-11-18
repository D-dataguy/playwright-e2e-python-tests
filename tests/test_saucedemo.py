import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

def test_login_success(page: Page, login_page: LoginPage, inventory_page: InventoryPage) -> None:
    login_page.login()
    inventory_page.expect_inventory_visible()

def test_login_locked_out_user_shows_error(login_page: LoginPage) -> None:
    login_page.navigate()
    login_page.enter_username("locked_out_user")
    login_page.enter_password("secret_sauce")
    login_page.click_login()
    login_page.expect_error_containing("Sorry, this user has been locked out")

def test_inventory_displays_products(logged_in_page: Page, inventory_page: InventoryPage) -> None:
    inventory_page.expect_all_products_displayed()

def test_add_single_item_to_cart_updates_badge(logged_in_page: Page, inventory_page: InventoryPage) -> None:
    inventory_page.add_to_cart("Sauce Labs Backpack")
    inventory_page.expect_cart_badge("1")

def test_add_multiple_items_to_cart(logged_in_page: Page, inventory_page: InventoryPage) -> None:
    inventory_page.add_to_cart("Sauce Labs Backpack")
    inventory_page.add_to_cart("Sauce Labs Bike Light")
    inventory_page.add_to_cart("Sauce Labs Bolt T-Shirt")
    inventory_page.expect_cart_badge("3")

def test_remove_item_from_inventory_page(logged_in_page: Page, inventory_page: InventoryPage) -> None:
    inventory_page.add_to_cart("Sauce Labs Backpack")
    inventory_page.expect_cart_badge("1")
    inventory_page.remove_from_cart("Sauce Labs Backpack")
    inventory_page.expect_cart_badge_absent()

def test_cart_page_shows_added_items(logged_in_page: Page, inventory_page: InventoryPage, cart_page: CartPage) -> None:
    inventory_page.add_to_cart("Sauce Labs Backpack")
    inventory_page.add_to_cart("Sauce Labs Bike Light")
    inventory_page.go_to_cart()
    cart_page.expect_item_present("Sauce Labs Backpack", "$29.99")
    cart_page.expect_item_present("Sauce Labs Bike Light", "$9.99")

def test_continue_shopping_returns_to_inventory(logged_in_page: Page, inventory_page: InventoryPage, cart_page: CartPage) -> None:
    inventory_page.go_to_cart()
    cart_page.click_continue_shopping()
    inventory_page.expect_inventory_visible()

def test_checkout_step_one_form_validation(logged_in_page: Page, inventory_page: InventoryPage, cart_page: CartPage, checkout_page: CheckoutPage) -> None:
    inventory_page.add_to_cart("Sauce Labs Backpack")
    inventory_page.go_to_cart()
    cart_page.click_checkout()
    checkout_page.continue_checkout()
    checkout_page.expect_error_containing("First Name is required")

def test_checkout_complete_flow(logged_in_page: Page, inventory_page: InventoryPage, cart_page: CartPage, checkout_page: CheckoutPage) -> None:
    inventory_page.add_to_cart("Sauce Labs Backpack")
    inventory_page.go_to_cart()
    cart_page.click_checkout()
    checkout_page.fill_step_one("John", "Doe", "12345")
    checkout_page.continue_checkout()
    checkout_page.expect_finish_button_present()
    checkout_page.complete_purchase()
    checkout_page.expect_order_complete()

def test_menu_logout(logged_in_page: Page, inventory_page: InventoryPage, login_page: LoginPage) -> None:
    inventory_page.logout()
    login_page.expect_login_button_visible()

def test_menu_reset_app_state(logged_in_page: Page, inventory_page: InventoryPage) -> None:
    inventory_page.add_to_cart("Sauce Labs Backpack")
    inventory_page.add_to_cart("Sauce Labs Bike Light")
    inventory_page.expect_cart_badge("2")
    inventory_page.reset_app()
    inventory_page.expect_cart_badge_absent()

def test_menu_about_link(logged_in_page: Page, inventory_page: InventoryPage) -> None:
    inventory_page.open_menu()
    expect(inventory_page.page.locator('[data-test="about-sidebar-link"]')).to_have_attribute("href", "https://saucelabs.com/")