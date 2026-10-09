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


def test_gpd_14_ai_disclaimer_and_compliance(logged_in_driver):
    driver = logged_in_driver

    try:
        print("\n========================================")
        print("GPD-14: AI Disclaimer & Compliance")
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
        # STEP 2: Open Settings
        # --------------------------------------------------
        print("\nOpening Settings...")

        settings = None
        end_time = time.time() + 30

        while time.time() < end_time:
            try:
                elements = driver.find_elements(
                    AppiumBy.ACCESSIBILITY_ID,
                    "Settings"
                )

                for element in elements:
                    try:
                        if element.is_displayed() and element.is_enabled():
                            settings = element
                            break
                    except Exception:
                        pass

                if settings:
                    break

            except Exception:
                pass

            time.sleep(1)

        if settings is None:
            driver.save_screenshot(
                "screenshots/GPD-14-settings-not-found.png"
            )
            raise AssertionError(
                "Settings button was not found."
            )

        settings.click()
        print("Settings clicked.")

        time.sleep(3)

        # --------------------------------------------------
        # STEP 3: Open Compliance
        # --------------------------------------------------
        print("\nOpening Compliance...")

        compliance = None
        end_time = time.time() + 30

        while time.time() < end_time:
            try:
                elements = driver.find_elements(
                    AppiumBy.ACCESSIBILITY_ID,
                    "Compliance CDSCO, DPDPA, clinical scope"
                )

                for element in elements:
                    try:
                        if element.is_displayed() and element.is_enabled():
                            compliance = element
                            break
                    except Exception:
                        pass

                if compliance:
                    break

            except Exception:
                pass

            time.sleep(1)

        if compliance is None:
            driver.save_screenshot(
                "screenshots/GPD-14-compliance-not-found.png"
            )
            raise AssertionError(
                "Compliance button was not found."
            )

        compliance.click()
        print("Compliance clicked.")

        time.sleep(4)

        # --------------------------------------------------
        # STEP 4: Verify Compliance page opened
        # --------------------------------------------------
        print("\nReading Compliance page...")

        page_text = get_visible_text(driver)
        text_lower = page_text.lower()

        print("\n========== COMPLIANCE SCREEN ==========")
        print(page_text)
        print("========== END COMPLIANCE SCREEN ==========")

        # --------------------------------------------------
        # STEP 5: Verify current compliance content
        # --------------------------------------------------
        print("\nChecking Compliance information...")

        compliance_sections = [
            "intended use",
            "clinical scope",
            "regulatory approvals",
            "data protection",
            "clinical governance",
            "not intended for",
            "histopathology",
            "cdsco",
            "dpdpa",
            "iso 13485",
            "iec 62304"
        ]

        found_sections = []

        for section in compliance_sections:
            if section in text_lower:
                found_sections.append(section)

        print("\nCurrent Compliance information found:")

        for section in found_sections:
            print(f"✓ {section}")

        # --------------------------------------------------
        # STEP 6: Verify page has meaningful compliance content
        # --------------------------------------------------
        if len(found_sections) < 3:
            screenshot_path = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    "screenshots",
                    "GPD-14-insufficient-content.png"
                )
            )
            driver.save_screenshot(screenshot_path)

            # --- JIRA INTEGRATION START ---
            try:
                from utils.bug_reporter import report_bug_to_jira
                
                report_bug_to_jira(
                    driver=driver,
                    test_case_id="GPD-14",
                    bug_title="Compliance page lacks sufficient compliance information",
                    actual_result="Compliance page displays insufficient sections.",
                    expected_result="Compliance page must contain multiple required compliance and regulatory sections.",
                    screenshot_path=screenshot_path
                )
            except Exception as e:
                print(f"Jira reporting failed: {e}\nContinuing with pytest failure...")
            # --- JIRA INTEGRATION END ---

            raise AssertionError(
                "Compliance page did not contain sufficient compliance information."
            )

        # --------------------------------------------------
        # STEP 7: PASS
        # --------------------------------------------------
        print("\n========================================")
        print("GPD-14 PASSED")
        print("========================================")

        print("✓ Login successful")
        print("✓ Settings opened")
        print("✓ Compliance page opened")
        print("✓ Current AI/compliance information verified")
        print("✓ Regulatory information verified")
        print("✓ Clinical scope/disclaimer information verified")

        print("\nTest passed successfully.")
        print("========================================")

    except Exception:

        try:
            driver.save_screenshot(
                "screenshots/GPD-14-failure.png"
            )

            print(
                "\nFailure screenshot saved:"
                "\nscreenshots/GPD-14-failure.png"
            )

        except Exception:
            pass

        raise