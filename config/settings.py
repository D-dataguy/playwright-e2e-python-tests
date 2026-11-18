"""Environment-based configuration for the test automation framework."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()

# Base URLs
SAUCEDEMO_BASE_URL = os.getenv("SAUCEDEMO_BASE_URL", "https://www.saucedemo.com").rstrip("/")
ORANGEHRM_BASE_URL = os.getenv(
    "ORANGEHRM_BASE_URL", "https://opensource-demo.orangehrmlive.com"
).rstrip("/")

# SauceDemo credentials
SAUCEDEMO_USERNAME = os.getenv("SAUCEDEMO_USERNAME", "standard_user")
SAUCEDEMO_PASSWORD = os.getenv("SAUCEDEMO_PASSWORD", "secret_sauce")

# OrangeHRM credentials
ORANGEHRM_USERNAME = os.getenv("ORANGEHRM_USERNAME", "Admin")
ORANGEHRM_PASSWORD = os.getenv("ORANGEHRM_PASSWORD", "admin123")

# Test execution settings
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
SLOW_MO = int(os.getenv("SLOW_MO", "0"))
TIMEOUT = int(os.getenv("TIMEOUT", "30000"))

# Output directories
BASE_DIR = Path(__file__).resolve().parent.parent
REPORTS_DIR = BASE_DIR / "reports"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
LOGS_DIR = BASE_DIR / "logs"
TEST_DATA_DIR = BASE_DIR / "test_data"

# Ensure output directories exist
REPORTS_DIR.mkdir(exist_ok=True)
SCREENSHOTS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)