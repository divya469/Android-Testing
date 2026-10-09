import os
import time
import pytest
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


def test_gpd_12_day_reports_and_clinical_audit(logged_in_driver):
    driver = logged_in_driver

    try:
        print("\n========================================")
        print("GPD-12: Day Reports & Clinical Audit")
        print("========================================")

        print("\nLogin completed successfully.")
        time.sleep(2)

        # --------------------------------------------------
        # STEP 1: Scroll down on Home screen
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
        # STEP 2: Click Day Reports
        # --------------------------------------------------
        print("\nOpening Day Reports...")

        driver.execute_script(
            "mobile: clickGesture",
            {
                "x": 675,
                "y": 2295
            }
        )

        print("Day Reports clicked.")

        time.sleep(4)

        # --------------------------------------------------
        # STEP 3: Verify Day Reports page
        # --------------------------------------------------
        print("\nWaiting for Day Reports page...")

        end_time = time.time() + 30
        page_text = ""

        while time.time() < end_time:

            page_text = get_visible_text(driver)

            if (
                "Day Reports" in page_text
                or "Reports" in page_text
                or "Total scans" in page_text
                or "Cancer" in page_text
            ):
                break

            time.sleep(1)

        print("\n========== DAY REPORTS SCREEN ==========")
        print(page_text)
        print("========== END DAY REPORTS SCREEN ==========")

        # --------------------------------------------------
        # STEP 4: Select Today
        # --------------------------------------------------
        print("\nSelecting Today...")

        today_found = False

        today_elements = driver.find_elements(
            AppiumBy.XPATH,
            "//*[@text='Today']"
        )

        for element in today_elements:
            try:
                if element.is_displayed():
                    element.click()
                    today_found = True
                    print("Today selected.")
                    break
            except Exception:
                pass

        if not today_found:
            print("Today option not found. Continuing with current date filter.")

        time.sleep(3)

        # --------------------------------------------------
        # STEP 5: Read daily report metrics
        # --------------------------------------------------
        print("\nChecking daily audit metrics...")

        page_text = get_visible_text(driver)

        print("\n========== DAILY REPORT ==========")
        print(page_text)
        print("========== END DAILY REPORT ==========")

        # Check for scan-related information
        scan_keywords = [
            "scan",
            "scans",
            "total",
            "cancer",
            "referral",
            "diagnosis"
        ]

        found_metrics = []

        for keyword in scan_keywords:
            if keyword.lower() in page_text.lower():
                found_metrics.append(keyword)

        print("\nMetrics found:")

        for metric in found_metrics:
            print(f"✓ {metric}")

        if not found_metrics:
            driver.save_screenshot(
                "screenshots/GPD-12-no-metrics.png"
            )

            raise AssertionError(
                "No daily audit metrics were displayed."
            )

        # --------------------------------------------------
        # STEP 6: Check Export Summary CSV
        # --------------------------------------------------
        print("\nChecking for Export Summary CSV...")

        export_elements = driver.find_elements(
            AppiumBy.XPATH,
            "//*[contains(@text,'Export Summary CSV')]"
        )

        export_found = False

        for element in export_elements:
            try:
                if element.is_displayed():
                    export_found = True
                    break
            except Exception:
                pass

        # --------------------------------------------------
        # STEP 7: BUG-06 validation
        # --------------------------------------------------
        if not export_found:

            print("\n========================================")
            print("BUG-06 REPRODUCED")
            print("========================================")

            print(
                "Daily report metrics are displayed, "
                "but 'Export Summary CSV' is not visible."
            )

            screenshot_path = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    "screenshots",
                    "GPD-12-export-bug.png"
                )
            )

            driver.save_screenshot(screenshot_path)

            print(
                "\nScreenshot saved:"
                f"\n{screenshot_path}"
            )

            print("\nExpected:")
            print("Export Summary CSV should be available.")

            print("\nActual:")
            print(
                "Export Summary CSV option is not available."
            )

            # --- JIRA INTEGRATION START ---
            try:
                from utils.bug_reporter import report_bug_to_jira
                
                report_bug_to_jira(
                    driver=driver,
                    test_case_id="GPD-12",
                    bug_title="Export Summary CSV option is not visible on Day Reports page",
                    actual_result="Export Summary CSV option is not available.",
                    expected_result="Export Summary CSV should be available.",
                    screenshot_path=screenshot_path
                )
            except Exception as e:
                print(f"Jira reporting failed: {e}\nContinuing with pytest failure...")
            # --- JIRA INTEGRATION END ---

            pytest.fail(
                "BUG-06: Export Summary CSV option is not visible "
                "on the Day Reports page."
            )

        # --------------------------------------------------
        # STEP 8: If export button exists
        # --------------------------------------------------
        print("\n✓ Export Summary CSV option found.")

        export_button = export_elements[0]

        export_button.click()

        print("Export Summary CSV clicked.")

        time.sleep(3)

        print("\n========================================")
        print("GPD-12 PASSED")
        print("========================================")

    except Exception:

        try:
            driver.save_screenshot(
                "screenshots/GPD-12-failure.png"
            )

            print(
                "\nFailure screenshot saved:"
                "\nscreenshots/GPD-12-failure.png"
            )

        except Exception:
            pass

        raise