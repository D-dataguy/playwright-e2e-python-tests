# Playwright Python E2E Tests

End-to-end tests using Python, pytest, and Playwright.

## Setup

```powershell
py -m venv .venv
.\\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\\.venv\Scripts\python.exe -m playwright install chromium
```

## Run tests

```powershell
.\\.venv\Scripts\python.exe -m pytest
```

## Test Suites

### OrangeHRM Dashboard (`tests/test_orangehrm_dashboard.py`)

Smoke test for the public OrangeHRM demo. Override with environment variables:

- `ORANGEHRM_BASE_URL` (default: `https://opensource-demo.orangehrmlive.com`)
- `ORANGEHRM_USERNAME` (default: `Admin`)
- `ORANGEHRM_PASSWORD` (default: `admin123`)

### SauceDemo (`tests/test_saucedemo.py`)

Comprehensive e2e tests for the Sauce Labs Swag Labs demo app. Override with:

- `SAUCEDEMO_BASE_URL` (default: `https://www.saucedemo.com`)
- `SAUCEDEMO_USERNAME` (default: `standard_user`)
- `SAUCEDEMO_PASSWORD` (default: `secret_sauce`)

Covers:
- Login (success + locked out user)
- Inventory page (all 6 products with names/prices)
- Cart (add/remove items, badge updates, cart page display)
- Checkout (form validation, complete purchase flow)
- Side menu (logout, reset app state, about link)

## Project Structure

```
.github/agents/    # VS Code agent configs (planner, generator, healer)
specs/             # Test plans
tests/             # Python test files
.venv/             # Virtual environment (gitignored)
```