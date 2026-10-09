import os
import time
from appium.webdriver.common.appiumby import AppiumBy


def get_visible_text(driver):
    texts = []

    try:
        elements = driver.find_elements(AppiumBy.XPATH, "//*[@text]")

        for element in elements:
            try:
                if element.is_displayed():
                    text = element.text
                    if text and text.strip():
                        texts.append(text.strip())
            except Exception:
                pass

    except Exception:
        pass

    return "\n".join(texts)


def test_gpd_13_subscription_and_scan_quota(logged_in_driver):
    driver = logged_in_driver

    try:
        print("\n========================================")
        print("GPD-13: Subscription & Scan Quota")
        print("========================================")

        print("\nLogin completed successfully.")
        time.sleep(2)

        # --------------------------------------------------
        # STEP 1: Scroll Home screen down
        # --------------------------------------------------
        print("\nScrolling Home screen down...")

        driver.execute_script(
            "mobile: swipeGesture",
            {
                "left": 100,
                "top": 500,
                "width": 880,
                "height": 1300,
                "direction": "up",
                "percent": 0.70
            }
        )

        time.sleep(2)

        print("Home screen scrolled.")

        # --------------------------------------------------
        # STEP 2: Click Settings
        # --------------------------------------------------
        print("\nOpening Settings...")

        settings = None

        end_time = time.time() + 30

        while time.time() < end_time:
            try:
                settings_elements = driver.find_elements(
                    AppiumBy.ACCESSIBILITY_ID,
                    "Settings"
                )

                for element in settings_elements:
                    if element.is_displayed() and element.is_enabled():
                        settings = element
                        break

                if settings:
                    break

            except Exception:
                pass

            time.sleep(1)

        if settings is None:
            driver.save_screenshot(
                "screenshots/GPD-13-settings-not-found.png"
            )
            raise AssertionError(
                "Settings navigation button was not found."
            )

        settings.click()

        print("Settings clicked.")
        time.sleep(3)

        # --------------------------------------------------
        # STEP 3: Click Subscription
        # --------------------------------------------------
        print("\nOpening Subscription...")

        subscription = None

        end_time = time.time() + 30

        while time.time() < end_time:
            try:
                subscription_elements = driver.find_elements(
                    AppiumBy.ACCESSIBILITY_ID,
                    "Subscription Plan, billing, scan quota"
                )

                for element in subscription_elements:
                    if element.is_displayed() and element.is_enabled():
                        subscription = element
                        break

                if subscription:
                    break

            except Exception:
                pass

            time.sleep(1)

        if subscription is None:
            driver.save_screenshot(
                "screenshots/GPD-13-subscription-not-found.png"
            )
            raise AssertionError(
                "Subscription button was not found."
            )

        subscription.click()

        print("Subscription clicked.")
        time.sleep(4)

        # --------------------------------------------------
        # STEP 4: Read Subscription page
        # --------------------------------------------------
        print("\nReading subscription details...")

        page_text = get_visible_text(driver)

        print("\n========== SUBSCRIPTION SCREEN ==========")
        print(page_text)
        print("========== END SUBSCRIPTION SCREEN ==========")

        # --------------------------------------------------
        # STEP 5: Verify subscription tier
        # --------------------------------------------------
        print("\nChecking subscription tier...")

        tier_found = False

        tier_keywords = [
            "GP Starter",
            "GP Practice",
            "Clinic",
            "Professional",
            "Trial"
        ]

        for tier in tier_keywords:
            if tier.lower() in page_text.lower():
                print(f"✓ Subscription tier found: {tier}")
                tier_found = True
                break

        if not tier_found:
            driver.save_screenshot(
                "screenshots/GPD-13-tier-not-found.png"
            )

            raise AssertionError(
                "Active subscription tier was not displayed."
            )

        # --------------------------------------------------
        # STEP 6: Verify scan quota
        # --------------------------------------------------
        print("\nChecking monthly scan quota...")

        quota_found = False

        quota_keywords = [
            "scans since",
            "scans/month",
            "scans",
            "scan"
        ]

        for keyword in quota_keywords:
            if keyword.lower() in page_text.lower():
                print(f"✓ Scan quota information found: {keyword}")
                quota_found = True
                break

        if not quota_found:
            screenshot_path = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    "screenshots",
                    "GPD-13-quota-not-found.png"
                )
            )
            driver.save_screenshot(screenshot_path)

            # --- JIRA INTEGRATION START ---
            try:
                from utils.bug_reporter import report_bug_to_jira
                
                report_bug_to_jira(
                    driver=driver,
                    test_case_id="GPD-13",
                    bug_title="Remaining scan quota is not displayed on Subscription page",
                    actual_result="Monthly scan quota information is missing.",
                    expected_result="Monthly scan quota should be displayed.",
                    screenshot_path=screenshot_path
                )
            except Exception as e:
                print(f"Jira reporting failed: {e}\nContinuing with pytest failure...")
            # --- JIRA INTEGRATION END ---

            raise AssertionError(
                "Monthly scan quota was not displayed."
            )

        # --------------------------------------------------
        # STEP 7: Final result
        # --------------------------------------------------
        print("\n========================================")
        print("GPD-13 PASSED")
        print("========================================")

        print("✓ Subscription details displayed")
        print("✓ Active subscription tier displayed")
        print("✓ Monthly scan information displayed")
        print("✓ Scan quota verified")

        print("========================================")

    except Exception:

        try:
            driver.save_screenshot(
                "screenshots/GPD-13-failure.png"
            )

            print(
                "\nFailure screenshot saved:"
                "\nscreenshots/GPD-13-failure.png"
            )

        except Exception:
            pass

        raise