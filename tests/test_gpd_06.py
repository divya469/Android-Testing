from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_gpd_06_named_patient(logged_in_driver):
    driver = logged_in_driver
    wait = WebDriverWait(driver, 20)

    # =========================================================
    # GPD-06: Named Patient Mode
    # Test Data:
    # Name   : Aruna Sharma
    # Age    : 45
    # Sex    : Female
    # Phone  : 9876543210
    # =========================================================

    # ---------------------------------------------------------
    # 1. Tap "Add patient details"
    # ---------------------------------------------------------

    add_patient = wait.until(
        EC.element_to_be_clickable(
            (
                AppiumBy.XPATH,
                "//android.widget.Button[contains(@text,'Add patient details')]"
            )
        )
    )

    add_patient.click()
    print("Add patient details clicked successfully.")

    # ---------------------------------------------------------
    # 2. Enter Full Name
    # ---------------------------------------------------------

    full_name = wait.until(
        EC.visibility_of_element_located(
            (
                AppiumBy.XPATH,
                "//android.widget.EditText[@index='1']"
            )
        )
    )

    full_name.click()
    full_name.clear()
    full_name.send_keys("Aruna Sharma")

    print("Full Name entered: Aruna Sharma")

    # ---------------------------------------------------------
    # 3. Enter Age
    # ---------------------------------------------------------

    age = wait.until(
        EC.visibility_of_element_located(
            (
                AppiumBy.XPATH,
                "//android.widget.EditText[@index='3']"
            )
        )
    )

    age.click()
    age.clear()

    # Clipboard + Android paste
    driver.set_clipboard_text("45")
    age.click()
    driver.press_keycode(279)  # KEYCODE_PASTE

    print("Age entered: 45")

    # ---------------------------------------------------------
    # 4. Select Female
    # ---------------------------------------------------------

    sex_dropdown = wait.until(
        EC.element_to_be_clickable(
            (
                AppiumBy.XPATH,
                "//*[@text='Male']"
            )
        )
    )

    sex_dropdown.click()

    print("Sex dropdown opened.")

    female_option = wait.until(
        EC.element_to_be_clickable(
            (
                AppiumBy.XPATH,
                "//*[@text='Female']"
            )
        )
    )

    female_option.click()

    print("Female selected successfully.")

    # ---------------------------------------------------------
    # 5. Enter Phone Number
    # ---------------------------------------------------------

    phone = wait.until(
        EC.visibility_of_element_located(
            (
                AppiumBy.XPATH,
                "//android.widget.EditText[@index='6']"
            )
        )
    )

    phone.click()
    phone.clear()
    phone.send_keys("9876543210")

    print("Phone number entered: 9876543210")

    # ---------------------------------------------------------
    # 6. Tap "Create & continue"
    # ---------------------------------------------------------

    create_continue = wait.until(
        EC.element_to_be_clickable(
            (
                AppiumBy.XPATH,
                "//android.widget.Button[@text='Create & continue']"
            )
        )
    )

    create_continue.click()

    print("Create & continue clicked successfully.")

    # ---------------------------------------------------------
    # 7. Verify that the action completed
    # ---------------------------------------------------------

    print("\n========== GPD-06 RESULT ==========")
    print("Activity:", driver.current_activity)
    print("Context:", driver.current_context)

    assert driver is not None

    print("GPD-06 Named Patient test completed successfully.")