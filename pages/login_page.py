import os
from dotenv import load_dotenv
from appium.webdriver.common.appiumby import AppiumBy

load_dotenv()


class LoginPage:

    def __init__(self, driver):
        self.driver = driver

    def login(self):
        email = os.getenv("MEDIKNO_EMAIL")
        password = os.getenv("MEDIKNO_PASSWORD")
        clinic = os.getenv("CLINIC_NAME")
        pin = os.getenv("MEDIKNO_PIN")

        from selenium.common.exceptions import StaleElementReferenceException
        import time

        # Email
        for _ in range(3):
            try:
                email_input = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")[0]
                email_input.send_keys(email)
                break
            except StaleElementReferenceException:
                time.sleep(1)

        # Password
        for _ in range(3):
            try:
                password_input = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")[1]
                password_input.send_keys(password)
                break
            except StaleElementReferenceException:
                time.sleep(1)

        # Sign In
        self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().text("Sign In")'
        ).click()

        # Select clinic/user
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        clinic_element = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{clinic}")'))
        )
        clinic_element.click()

        # Enter PIN digit by digit
        for digit in pin:
            self.driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiSelector().text("{digit}")'
            ).click()