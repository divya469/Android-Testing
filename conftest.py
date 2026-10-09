import os
import time

import pytest
from dotenv import load_dotenv

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
    NoSuchElementException,
)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# COMMON CONFIGURATION
# ============================================================

APP_PACKAGE = os.getenv(
    "APP_PACKAGE",
    "in.medikno.gpderma"
)

APP_ACTIVITY = os.getenv(
    "APP_ACTIVITY",
    "in.medikno.consumer.MainActivity"
)

DEVICE_NAME = os.getenv(
    "DEVICE_NAME",
    "emulator-5554"
)

APPIUM_SERVER = os.getenv(
    "APPIUM_SERVER",
    "http://127.0.0.1:4723"
)

MEDIKNO_EMAIL = os.getenv(
    "MEDIKNO_EMAIL"
)

MEDIKNO_PASSWORD = os.getenv(
    "MEDIKNO_PASSWORD"
)


# ============================================================
# DRIVER FIXTURE
# ============================================================

@pytest.fixture
def driver():

    options = UiAutomator2Options()

    options.platform_name = "Android"

    options.device_name = DEVICE_NAME

    options.app_package = APP_PACKAGE

    options.app_activity = APP_ACTIVITY

    options.automation_name = "UiAutomator2"

    # --------------------------------------------------------
    # Appium / UiAutomator2 timeouts
    # --------------------------------------------------------

    options.set_capability(
        "uiautomator2ServerLaunchTimeout",
        60000
    )

    options.set_capability(
        "uiautomator2ServerInstallTimeout",
        60000
    )

    options.set_capability(
        "adbExecTimeout",
        60000
    )

    # --------------------------------------------------------
    # Create Appium session
    # --------------------------------------------------------

    driver = webdriver.Remote(
        APPIUM_SERVER,
        options=options
    )

    # Common implicit wait
    driver.implicitly_wait(10)

    print("\n========================================")
    print("Appium session started")
    print(f"Device: {DEVICE_NAME}")
    print(f"Package: {APP_PACKAGE}")
    print(f"Activity: {APP_ACTIVITY}")
    print("========================================\n")

    yield driver

    # --------------------------------------------------------
    # Close session
    # --------------------------------------------------------

    try:
        driver.quit()
        print("\nAppium session closed.")
    except Exception:
        pass


# ============================================================
# HELPER: GET PAGE SOURCE
# ============================================================

def get_page_source(driver):

    try:
        return driver.page_source.lower()
    except Exception:
        return ""


# ============================================================
# HELPER: CHECK WHETHER TEXT EXISTS ON SCREEN
# ============================================================

def screen_contains(driver, text):

    try:
        return text.lower() in get_page_source(driver)
    except Exception:
        return False


# ============================================================
# HELPER: CHECK WHETHER DASHBOARD IS OPEN
# ============================================================

def is_dashboard(driver):

    source = get_page_source(driver)

    dashboard_indicators = [
        "anonymous patient",
        "add patient details",
        "start a new scan",
        "recent scans",
        "choose patient",
    ]

    return any(
        indicator in source
        for indicator in dashboard_indicators
    )


# ============================================================
# HELPER: CHECK WHETHER LOGIN SCREEN IS OPEN
# ============================================================

def is_login_screen(driver):

    try:

        email_fields = driver.find_elements(
            AppiumBy.XPATH,
            "//android.widget.EditText[@hint='Email']"
        )

        password_fields = driver.find_elements(
            AppiumBy.XPATH,
            "//android.widget.EditText[@hint='Password']"
        )

        return (
            len(email_fields) > 0
            or len(password_fields) > 0
        )

    except Exception:

        return False


# ============================================================
# HELPER: HANDLE ONBOARDING
# ============================================================

def handle_onboarding(driver):

    print("\nChecking onboarding screen...")

    # --------------------------------------------------------
    # FIRST NEXT
    # --------------------------------------------------------

    try:

        next_button = WebDriverWait(
            driver,
            5
        ).until(
            EC.element_to_be_clickable(
                (
                    AppiumBy.XPATH,
                    "//android.widget.Button[@text='Next']"
                )
            )
        )

        next_button.click()

        print("First Next clicked.")

    except TimeoutException:

        print("First Next not required.")

    # --------------------------------------------------------
    # SECOND NEXT
    # --------------------------------------------------------

    try:

        next_button = WebDriverWait(
            driver,
            5
        ).until(
            EC.element_to_be_clickable(
                (
                    AppiumBy.XPATH,
                    "//android.widget.Button[@text='Next']"
                )
            )
        )

        next_button.click()

        print("Second Next clicked.")

    except TimeoutException:

        print("Second Next not required.")

    # --------------------------------------------------------
    # GET STARTED
    # --------------------------------------------------------

    try:

        get_started = WebDriverWait(
            driver,
            5
        ).until(
            EC.element_to_be_clickable(
                (
                    AppiumBy.XPATH,
                    "//android.widget.Button[@text='Get started']"
                )
            )
        )

        get_started.click()

        print("Get started clicked.")

    except TimeoutException:

        print("Get started not required.")

    time.sleep(2)


# ============================================================
# HELPER: LOGIN
# ============================================================

def perform_login(driver):

    if not MEDIKNO_EMAIL:
        raise RuntimeError(
            "MEDIKNO_EMAIL is not set in .env"
        )

    if not MEDIKNO_PASSWORD:
        raise RuntimeError(
            "MEDIKNO_PASSWORD is not set in .env"
        )

    wait = WebDriverWait(
        driver,
        30
    )

    # --------------------------------------------------------
    # EMAIL
    # --------------------------------------------------------

    email_locator = (
        AppiumBy.XPATH,
        "//android.widget.EditText[@hint='Email']"
    )

    for attempt in range(3):

        try:

            email_field = wait.until(
                EC.visibility_of_element_located(
                    email_locator
                )
            )

            email_field.click()

            email_field.clear()

            email_field.send_keys(
                MEDIKNO_EMAIL
            )

            print("Email entered successfully.")

            break

        except StaleElementReferenceException:

            print(
                f"Email field stale. "
                f"Retry {attempt + 1}/3..."
            )

            time.sleep(1)

    else:

        raise RuntimeError(
            "Unable to enter email."
        )

    # --------------------------------------------------------
    # PASSWORD
    # --------------------------------------------------------

    password_locator = (
        AppiumBy.XPATH,
        "//android.widget.EditText[@hint='Password']"
    )

    for attempt in range(3):

        try:

            password_field = wait.until(
                EC.visibility_of_element_located(
                    password_locator
                )
            )

            password_field.click()

            password_field.clear()

            password_field.send_keys(
                MEDIKNO_PASSWORD
            )

            print(
                "Password entered successfully."
            )

            break

        except StaleElementReferenceException:

            print(
                f"Password field stale. "
                f"Retry {attempt + 1}/3..."
            )

            time.sleep(1)

    else:

        raise RuntimeError(
            "Unable to enter password."
        )

    # --------------------------------------------------------
    # HIDE KEYBOARD
    # --------------------------------------------------------

    try:

        driver.hide_keyboard()

        print("Keyboard hidden.")

    except Exception:

        print(
            "Keyboard already hidden."
        )

    time.sleep(1)

    # --------------------------------------------------------
    # SIGN IN
    # --------------------------------------------------------

    sign_in_locator = (
        AppiumBy.XPATH,
        "//android.widget.Button[contains(@text,'Sign In')]"
    )

    for attempt in range(3):

        try:

            sign_in_button = wait.until(
                EC.element_to_be_clickable(
                    sign_in_locator
                )
            )

            sign_in_button.click()

            print(
                "Sign In clicked successfully."
            )

            break

        except (
            StaleElementReferenceException,
            TimeoutException
        ):

            print(
                f"Sign In not ready. "
                f"Retry {attempt + 1}/3..."
            )

            time.sleep(1)

    else:

        print(
            "\n========== LOGIN ERROR =========="
        )

        print(
            driver.page_source
        )

        print(
            "========== END LOGIN ERROR ==========\n"
        )

        raise RuntimeError(
            "Unable to click Sign In."
        )

    # --------------------------------------------------------
    # WAIT FOR DASHBOARD
    # --------------------------------------------------------

    print(
        "\nWaiting for dashboard..."
    )

    try:

        WebDriverWait(
            driver,
            40
        ).until(
            lambda d: is_dashboard(d)
        )

        print(
            "Login completed successfully."
        )

    except TimeoutException:

        print(
            "\nDashboard was not detected "
            "after login."
        )

        print(
            driver.page_source
        )

        raise RuntimeError(
            "Login attempted but dashboard "
            "was not detected."
        )


# ============================================================
# MAIN LOGIN FIXTURE
# ============================================================

@pytest.fixture
def logged_in_driver(driver):

    print(
        "\n========================================"
    )

    print(
        "Preparing logged-in GP-Derma session..."
    )

    print(
        "========================================"
    )

    # --------------------------------------------------------
    # Give app time to load
    # --------------------------------------------------------

    time.sleep(2)

    # ========================================================
    # CASE 1: ALREADY LOGGED IN
    # ========================================================

    if is_dashboard(driver):

        print(
            "Dashboard already visible."
        )

        print(
            "Login not required."
        )

        return driver

    # ========================================================
    # CASE 2: LOGIN SCREEN ALREADY VISIBLE
    # ========================================================

    if is_login_screen(driver):

        print(
            "Login screen detected."
        )

        perform_login(driver)

        return driver

    # ========================================================
    # CASE 3: ONBOARDING SCREEN
    # ========================================================

    print(
        "Login/dashboard not detected."
    )

    print(
        "Checking onboarding..."
    )

    handle_onboarding(driver)

    # ========================================================
    # CHECK AGAIN AFTER ONBOARDING
    # ========================================================

    time.sleep(2)

    # --------------------------------------------------------
    # Dashboard appeared
    # --------------------------------------------------------

    if is_dashboard(driver):

        print(
            "Dashboard detected after onboarding."
        )

        print(
            "Login not required."
        )

        return driver

    # --------------------------------------------------------
    # Login screen appeared
    # --------------------------------------------------------

    if is_login_screen(driver):

        print(
            "Login screen detected "
            "after onboarding."
        )

        perform_login(driver)

        return driver

    # ========================================================
    # UNKNOWN STATE
    # ========================================================

    print(
        "\n========== UNKNOWN APP STATE =========="
    )

    print(
        driver.page_source
    )

    print(
        "========== END UNKNOWN STATE ==========\n"
    )

    screenshot_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "screenshots",
            "unknown-app-state.png"
        )
    )

    os.makedirs(
        os.path.dirname(screenshot_path),
        exist_ok=True
    )

    driver.save_screenshot(
        screenshot_path
    )

    raise RuntimeError(
        "Unable to determine GP-Derma app state. "
        "Neither dashboard, login screen, nor onboarding "
        "was detected."
    )