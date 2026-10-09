import os
import time
import pytest

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# ============================================================
# TEST DATA
# ============================================================

TEST_IMAGE_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "test_data",
        "mole.jpg"
    )
)

BUG_ID = "BUG-03"

EXPECTED_VERDICTS = [
    "Urgent Dermatologist Excision",
    "Benign / Monitor"
]


# ============================================================
# GET VISIBLE TEXT
# ============================================================

def get_visible_text(driver):

    texts = []

    elements = driver.find_elements(
        AppiumBy.XPATH,
        "//*[@text]"
    )

    for element in elements:

        try:
            if element.is_displayed():

                text = (element.text or "").strip()

                if text:
                    texts.append(text)

        except Exception:
            continue

    # Remove duplicates
    unique_texts = []

    for text in texts:

        if text not in unique_texts:
            unique_texts.append(text)

    return "\n".join(unique_texts)


# ============================================================
# WAIT FOR ANALYZE BUTTON
# ============================================================

def wait_for_analyze_button(driver, timeout=60):

    print(
        f"\nWaiting up to {timeout} seconds "
        f"for Analyze button..."
    )

    end_time = time.time() + timeout

    while time.time() < end_time:

        try:

            buttons = driver.find_elements(
                AppiumBy.XPATH,
                "//android.widget.Button"
            )

            for button in buttons:

                try:

                    if not button.is_displayed():
                        continue

                    text = (
                        button.text or ""
                    ).strip()

                    print(
                        f"Visible button: '{text}'"
                    )

                    if "analyze" in text.lower():

                        print(
                            f"Analyze button found: '{text}'"
                        )

                        return button

                except Exception:
                    continue

        except Exception:
            pass

        time.sleep(2)

    return None


# ============================================================
# WAIT FOR AI REPORT
# ============================================================

def wait_for_ai_report(driver, timeout=120):

    print(
        f"\nWaiting up to {timeout} seconds "
        f"for AI report..."
    )

    end_time = time.time() + timeout

    last_report = ""

    while time.time() < end_time:

        try:

            report = get_visible_text(driver)

            if report != last_report:

                print(
                    "\n----- Report status -----"
                )

                print(report)

                print(
                    "----- End status -----"
                )

                last_report = report

            report_lower = report.lower()

            # Still processing
            if (
                "analyzing…" in report_lower
                or
                "analyzing..." in report_lower
            ):

                print(
                    "AI analysis still running..."
                )

            # Possible completed report
            if (
                "melanoma" in report_lower
                or
                "biopsy" in report_lower
                or
                "benign" in report_lower
                or
                "malignant" in report_lower
            ):

                print(
                    "\nAI report appears to be ready."
                )

                return report

        except Exception as e:

            print(
                f"Error checking AI report: {e}"
            )

        time.sleep(3)

    print(
        "\nAI report did not complete within "
        f"{timeout} seconds."
    )

    return last_report


# ============================================================
# SCROLL REPORT
# ============================================================

def scroll_report(driver, count=6):

    print(
        "\nScrolling report..."
    )

    for i in range(count):

        try:

            driver.execute_script(
                "mobile: swipeGesture",
                {
                    "left": 100,
                    "top": 400,
                    "width": 900,
                    "height": 1500,
                    "direction": "up",
                    "percent": 0.75
                }
            )

            time.sleep(1)

            print(
                f"Report scroll "
                f"{i + 1}/{count} completed."
            )

        except Exception as e:

            print(
                f"Scroll {i + 1} failed: {e}"
            )


# ============================================================
# GPD-08
# SKIN CANCER SCREENING
# ============================================================

def test_gpd_08_skin_cancer_screening(logged_in_driver):

    driver = logged_in_driver
    wait = WebDriverWait(driver, 30)

    try:

        # ====================================================
        # 1. ANONYMOUS PATIENT
        # ====================================================

        anonymous_patient = wait.until(
            EC.element_to_be_clickable(
                (
                    AppiumBy.XPATH,
                    "//android.widget.Button"
                    "[contains(@text,'Anonymous patient')]"
                )
            )
        )

        anonymous_patient.click()

        print(
            "Anonymous patient selected."
        )

        # ====================================================
        # 2. CREATE SESSION
        # ====================================================

        create_continue = wait.until(
            EC.element_to_be_clickable(
                (
                    AppiumBy.XPATH,
                    "//android.widget.Button"
                    "[@text='Create & continue']"
                )
            )
        )

        create_continue.click()

        print(
            "Anonymous patient session "
            "created successfully."
        )

        # ====================================================
        # 3. SELECT SKIN CANCER SCREENING
        # ====================================================

        skin_cancer_screening = wait.until(
            EC.element_to_be_clickable(
                (
                    AppiumBy.XPATH,
                    "//android.widget.Button"
                    "[contains(@text,'Skin cancer screening')]"
                )
            )
        )

        skin_cancer_screening.click()

        print(
            "Skin Cancer Screening selected."
        )

        time.sleep(2)

        print(
            "Skin Cancer Screening screen opened."
        )

        # ====================================================
        # 4. CHECK TEST IMAGE
        # ====================================================

        if not os.path.exists(TEST_IMAGE_PATH):

            raise FileNotFoundError(
                f"Test image not found:\n"
                f"{TEST_IMAGE_PATH}"
            )

        print(
            f"Test image found: "
            f"{TEST_IMAGE_PATH}"
        )

        # ====================================================
        # 5. UPLOAD FILE
        # ====================================================

        upload_file = wait.until(
            EC.presence_of_element_located(
                (
                    AppiumBy.XPATH,
                    "//*[contains(@text,'Upload file')]/.."
                )
            )
        )

        upload_file.click()

        print(
            "Upload file option clicked."
        )

        # ====================================================
        # 6. MORE OPTIONS
        # ====================================================

        more_options = WebDriverWait(
            driver,
            10
        ).until(
            EC.element_to_be_clickable(
                (
                    AppiumBy.ACCESSIBILITY_ID,
                    "More options"
                )
            )
        )

        more_options.click()

        print(
            "More options opened."
        )

        # ====================================================
        # 7. BROWSE
        # ====================================================

        browse = WebDriverWait(
            driver,
            10
        ).until(
            EC.presence_of_element_located(
                (
                    AppiumBy.XPATH,
                    "//*[@text='Browse…']"
                )
            )
        )

        browse.click()

        print(
            "Browse selected."
        )

        # ====================================================
        # 8. FIND MOLE.JPG
        # ====================================================

        print(
            "Searching for mole.jpg..."
        )

        mole_file = WebDriverWait(
            driver,
            20
        ).until(
            EC.presence_of_element_located(
                (
                    AppiumBy.XPATH,
                    "//android.widget.TextView"
                    "[@text='mole.jpg']"
                )
            )
        )

        print(
            "mole.jpg found in Android file picker."
        )

        # ====================================================
        # 9. SELECT MOLE.JPG
        # ====================================================

        try:

            mole_file_row = mole_file.find_element(
                AppiumBy.XPATH,
                ".."
            )

            print(
                f"mole.jpg parent bounds: "
                f"{mole_file_row.rect}"
            )

            driver.execute_script(
                "mobile: clickGesture",
                {
                    "elementId": mole_file_row.id
                }
            )

            print(
                "mole.jpg selected successfully."
            )

        except Exception:

            print(
                "Parent row selection failed."
            )

            print(
                "Trying filename directly..."
            )

            driver.execute_script(
                "mobile: clickGesture",
                {
                    "elementId": mole_file.id
                }
            )

            print(
                "mole.jpg clicked directly."
            )

        # ====================================================
        # 10. WAIT FOR RETURN TO APP
        # ====================================================

        time.sleep(3)

        print(
            "Returned from Android file picker."
        )

        # ====================================================
        # 11. WAIT FOR ANALYZE BUTTON
        # ====================================================

        analyze_button = wait_for_analyze_button(
            driver,
            timeout=60
        )

        if analyze_button is None:

            screenshot_path = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    "screenshots",
                    "GPD-08-no-analyze-button.png"
                )
            )

            os.makedirs(
                os.path.dirname(
                    screenshot_path
                ),
                exist_ok=True
            )

            driver.save_screenshot(
                screenshot_path
            )

            print(
                f"Screenshot saved: "
                f"{screenshot_path}"
            )

            print(
                "\n========== SCREEN TEXT =========="
            )

            print(
                get_visible_text(driver)
            )

            print(
                "\n========== END SCREEN TEXT =========="
            )

            pytest.fail(
                "Analyze button was not found within "
                "60 seconds after uploading mole.jpg."
            )

        # ====================================================
        # 12. CLICK ANALYZE
        # ====================================================

        analyze_button.click()

        print(
            "Analyze button clicked."
        )

        # ====================================================
        # 13. WAIT FOR AI REPORT
        # ====================================================

        report_text = wait_for_ai_report(
            driver,
            timeout=120
        )

        print(
            "\n========== INITIAL GPD-08 REPORT =========="
        )

        print(
            report_text
        )

        print(
            "\n========== END INITIAL REPORT =========="
        )

        # ====================================================
        # 14. CHECK IF STILL ANALYZING
        # ====================================================

        report_lower = report_text.lower()

        still_analyzing = (
            "analyzing…" in report_lower
            or
            "analyzing..." in report_lower
        )

        if still_analyzing and "melanoma" not in report_lower:

            screenshot_path = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    "screenshots",
                    "GPD-08-analysis-timeout.png"
                )
            )

            os.makedirs(
                os.path.dirname(
                    screenshot_path
                ),
                exist_ok=True
            )

            driver.save_screenshot(
                screenshot_path
            )

            print(
                f"Analysis timeout screenshot saved: "
                f"{screenshot_path}"
            )

            pytest.fail(
                "AI analysis did not complete within "
                "120 seconds."
            )

        # ====================================================
        # 15. SCROLL REPORT
        # ====================================================

        scroll_report(
            driver,
            count=6
        )

        # ====================================================
        # 16. GET FINAL REPORT
        # ====================================================

        final_report = get_visible_text(
            driver
        )

        print(
            "\n========== FINAL GPD-08 REPORT =========="
        )

        print(
            final_report
        )

        print(
            "\n========== END FINAL REPORT =========="
        )

        report_lower = final_report.lower()

        # ====================================================
        # 17. VALIDATE MELANOMA
        # ====================================================

        melanoma_present = (
            "melanoma"
            in report_lower
        )

        suspected_melanoma_present = (
            "suspected malignant melanoma"
            in report_lower
        )

        # ====================================================
        # 18. VALIDATE ABCDE
        # ====================================================

        abcde_keywords = [
            "asymmetry",
            "border",
            "color",
            "colour",
            "diameter",
            "abcde"
        ]

        abcde_found = []

        for keyword in abcde_keywords:

            if keyword in report_lower:

                abcde_found.append(
                    keyword
                )

        # ====================================================
        # 19. VALIDATE BIOPSY
        # ====================================================

        biopsy_present = (
            "biopsy"
            in report_lower
        )

        biopsy_recommended = (
            "biopsy recommended"
            in report_lower
        )

        # ====================================================
        # 20. VALIDATE REQUIRED VERDICT
        # ====================================================

        verdicts_found = []

        for verdict in EXPECTED_VERDICTS:

            if verdict.lower() in report_lower:

                verdicts_found.append(
                    verdict
                )

        explicit_verdict_present = (
            len(verdicts_found) > 0
        )

        # ====================================================
        # 21. PRINT VALIDATION
        # ====================================================

        print(
            "\n========== GPD-08 VALIDATION =========="
        )

        print(
            f"Melanoma diagnosis found: "
            f"{melanoma_present}"
        )

        print(
            f"Suspected malignant melanoma: "
            f"{suspected_melanoma_present}"
        )

        print(
            f"ABCDE findings found: "
            f"{abcde_found}"
        )

        print(
            f"Biopsy information found: "
            f"{biopsy_present}"
        )

        print(
            f"Biopsy recommended found: "
            f"{biopsy_recommended}"
        )

        print(
            f"Explicit biopsy verdict found: "
            f"{explicit_verdict_present}"
        )

        print(
            f"Verdicts found: "
            f"{verdicts_found}"
        )

        # ====================================================
        # 22. BUG-03 DETECTION
        # ====================================================

        bug_03_detected = (
            melanoma_present
            and biopsy_present
            and not explicit_verdict_present
        )

        # ====================================================
        # 23. BUG-03 SCREENSHOT
        # ====================================================

        if bug_03_detected:

            screenshot_path = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    "screenshots",
                    "GPD-08-BUG-03.png"
                )
            )

            os.makedirs(
                os.path.dirname(
                    screenshot_path
                ),
                exist_ok=True
            )

            driver.save_screenshot(
                screenshot_path
            )

            print(
                f"\n{BUG_ID} reproduced."
            )

            print(
                f"Screenshot saved: "
                f"{screenshot_path}"
            )

            # --- JIRA INTEGRATION START ---
            try:
                from utils.bug_reporter import report_bug_to_jira
                
                report_bug_to_jira(
                    driver=driver,
                    test_case_id="GPD-08",
                    bug_title="Explicit biopsy verdict missing in melanoma screening",
                    actual_result=(
                        "Skin cancer screening generated melanoma/biopsy findings, "
                        "but the required explicit biopsy verdict was not displayed."
                    ),
                    expected_result="Explicit biopsy verdict should be displayed.",
                    screenshot_path=screenshot_path
                )
            except Exception as e:
                print(f"Jira reporting failed: {e}\nContinuing with pytest failure...")
            # --- JIRA INTEGRATION END ---

            # BUG-03 is an expected application defect.
            # Therefore pytest FAIL is intentional.

            pytest.fail(
                f"{BUG_ID}: Skin cancer screening "
                f"generated melanoma/biopsy findings, "
                f"but the required explicit biopsy verdict "
                f"was not displayed."
            )

        # ====================================================
        # 24. EXPECTED PASS
        # ====================================================

        assert melanoma_present, (
            "Expected melanoma diagnosis was not found."
        )

        assert biopsy_present, (
            "Expected biopsy information was not found."
        )

        assert explicit_verdict_present, (
            "Expected explicit biopsy verdict was not found."
        )

        print(
            "\nGPD-08 passed successfully."
        )

    except Exception:

        failure_screenshot = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "screenshots",
                "GPD-08-automation-failure.png"
            )
        )

        try:

            os.makedirs(
                os.path.dirname(
                    failure_screenshot
                ),
                exist_ok=True
            )

            driver.save_screenshot(
                failure_screenshot
            )

            print(
                f"Failure screenshot saved: "
                f"{failure_screenshot}"
            )

        except Exception:
            pass

        raise