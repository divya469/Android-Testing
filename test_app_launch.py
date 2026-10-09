from appium import webdriver
from appium.options.android import UiAutomator2Options


def test_gp_derma_launch():

    options = UiAutomator2Options()

    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = "emulator-5554"

    options.app_package = "in.medikno.gpderma"
    options.app_activity = "in.medikno.consumer.MainActivity"

    driver = webdriver.Remote(
        "http://127.0.0.1:4723",
        options=options
    )

    driver.implicitly_wait(10)

    print("GP Derma app launched successfully!")

    driver.quit()