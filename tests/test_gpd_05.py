from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_gpd_05_anonymous_patient(logged_in_driver):

    driver = logged_in_driver
    wait = WebDriverWait(driver, 20)

    # -----------------------------------------
    # Step 1: Verify Anonymous Patient option
    # -----------------------------------------
    anonymous_patient = wait.until(
        EC.element_to_be_clickable(
            (
                AppiumBy.XPATH,
                "//android.widget.Button[contains(@text,'Anonymous patient')]"
            )
        )
    )

    print("Anonymous patient option found.")

    anonymous_patient.click()

    # -----------------------------------------
    # Step 2: Create & Continue
    # -----------------------------------------
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

    # -----------------------------------------
    # Step 3: Verify next screen
    # -----------------------------------------
    print("\n========== AFTER CREATE & CONTINUE ==========")
    print("Activity:", driver.current_activity)
    print("Context:", driver.current_context)

    print("Anonymous patient session created successfully.")