
import os
import time
import pytest

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# =========================================================
# GPD-07 TEST DATA
# =========================================================

PATIENT_AGE = "45"
PATIENT_SEX = "Female"
LESION_DURATION = "3 months"

TEST_IMAGE_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "test_data",
        "rash.jpg"
    )
)

SCREENSHOT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "screenshots")
)

BUG_ID = "BUG-02"


# =========================================================
# HELPER: GET VISIBLE TEXT
# =========================================================

def get_report_text(driver):
    texts = []

    try:
        elements = driver.find_elements(
            AppiumBy.XPATH, "//*[@text]"
        )

        for element in elements:
            try:
                if element.is_displayed():
                    value = element.text
                    if value and value.strip():
                        texts.append(value.strip())
            except Exception:
                pass

    except Exception:
        pass

    # Also inspect the complete accessibility source in case
    # some report text is not exposed as a separate element.
    try:
        source = driver.page_source
        if source:
            texts.append(source)
    except Exception:
        pass

    return "\n".join(texts)


# =========================================================
# HELPER: WAIT FOR AI ANALYSIS
# =========================================================

def wait_for_ai_report(driver, timeout=120):
    print(
        f"\nWaiting up to {timeout} seconds for AI analysis..."
    )

    end_time = time.monotonic() + timeout
    last_text = ""

    diagnosis_terms = [
        "plaque psoriasis",
        "eczema",
        "dermatitis",
        "diagnosis",
        "clinical analysis"
    ]

    while time.monotonic() < end_time:
        last_text = get_report_text(driver)
        lower_text = last_text.lower()

        # Wait until the report contains meaningful analysis
        # and the loading indicator is no longer displayed.
        analysis_visible = (
            "analyzing..." in lower_text
            or "analyzing…" in lower_text
        )

        report_found = any(
            term in lower_text for term in diagnosis_terms
        )

        if report_found and not analysis_visible:
            print("AI report content detected.")
            return last_text

        time.sleep(3)

    screenshot_path = os.path.join(
        SCREENSHOT_DIR,
        "GPD-07-analysis-timeout.png"
    )

    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    try:
        driver.save_screenshot(screenshot_path)
    except Exception:
        pass

    raise AssertionError(
        f"AI analysis did not produce a detectable report "
        f"within {timeout} seconds. "
        f"Last visible report text: {last_text[:1500]}"
    )


# =========================================================
# HELPER: SCROLL REPORT
# =========================================================

def scroll_report(driver):
    print("\nScrolling report to inspect treatment sections...")

    for index in range(5):
        try:
            driver.execute_script(
                "mobile: swipeGesture",
                {
                    "left": 100,
                    "top": 500,
                    "width": 880,
                    "height": 1300,
                    "direction": "up",
                    "percent": 0.65
                }
            )
        except Exception as error:
            print(f"Scroll attempt {index + 1}: {error}")

        time.sleep(1)


# =========================================================
# GPD-07 TEST
# =========================================================

def test_gpd_07_targeted_skin_lesion(logged_in_driver):
    driver = logged_in_driver
    wait = WebDriverWait(driver, 30)

    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    try:
        print("\n========================================")
        print("GPD-07: Targeted Skin Lesion Scan")
        print("========================================")

        # -------------------------------------------------
        # 1. SELECT ANONYMOUS PATIENT
        # -------------------------------------------------

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
        print("Anonymous patient selected.")

        # -------------------------------------------------
        # 2. CREATE ANONYMOUS SESSION
        # -------------------------------------------------

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

        print("Anonymous patient session created.")
        time.sleep(2)

        # -------------------------------------------------
        # 3. SELECT TARGETED SKIN LESION
        # -------------------------------------------------

        targeted_scan = wait.until(
            EC.element_to_be_clickable(
                (
                    AppiumBy.XPATH,
                    "//android.widget.Button"
                    "[contains(@text,'Targeted skin lesion')]"
                )
            )
        )
        targeted_scan.click()

        print("Targeted Skin Lesion selected.")

        # -------------------------------------------------
        # 4. VERIFY SCAN SCREEN
        # -------------------------------------------------

        wait.until(
            EC.visibility_of_element_located(
                (
                    AppiumBy.XPATH,
                    "//*[@text='Capture photo']"
                )
            )
        )

        print("Targeted Skin Lesion screen opened.")

        # -------------------------------------------------
        # 5. VERIFY LOCAL TEST IMAGE
        # -------------------------------------------------

        if not os.path.isfile(TEST_IMAGE_PATH):
            raise FileNotFoundError(
                f"Test image not found: {TEST_IMAGE_PATH}"
            )

        print(f"Test image found: {TEST_IMAGE_PATH}")

        # -------------------------------------------------
        # 6. OPEN UPLOAD FILE
        # -------------------------------------------------

        upload_file = wait.until(
            EC.presence_of_element_located(
                (
                    AppiumBy.XPATH,
                    "//android.widget.TextView"
                    "[@text='Upload file']/.."
                )
            )
        )
        upload_file.click()

        print("Upload file option clicked.")

        # -------------------------------------------------
        # 7. OPEN MORE OPTIONS
        # -------------------------------------------------

        more_options = WebDriverWait(
            driver, 15
        ).until(
            EC.element_to_be_clickable(
                (
                    AppiumBy.ACCESSIBILITY_ID,
                    "More options"
                )
            )
        )
        more_options.click()

        print("More options opened.")

        # -------------------------------------------------
        # 8. SELECT BROWSE
        # -------------------------------------------------

        browse = WebDriverWait(
            driver, 15
        ).until(
            EC.presence_of_element_located(
                (
                    AppiumBy.XPATH,
                    "//*[@text='Browse…']"
                )
            )
        )
        browse.click()

        print("Browse selected.")
        time.sleep(2)

        # -------------------------------------------------
        # 9. FIND rash.jpg BY NAME
        # -------------------------------------------------

        print("\nSearching specifically for rash.jpg...")

        rash_file = WebDriverWait(
            driver, 30
        ).until(
            EC.presence_of_element_located(
                (
                    AppiumBy.XPATH,
                    "//*[@text='rash.jpg']"
                )
            )
        )

        if not rash_file.is_displayed():
            raise AssertionError(
                "rash.jpg was found but is not displayed."
            )

        print("rash.jpg found and displayed.")

        # -------------------------------------------------
        # 10. SELECT rash.jpg
        # -------------------------------------------------

        try:
            rash_file.click()
        except Exception:
            rash_row = rash_file.find_element(
                AppiumBy.XPATH, ".."
            )

            driver.execute_script(
                "mobile: clickGesture",
                {"elementId": rash_row.id}
            )

        print("rash.jpg selected.")
        time.sleep(4)

        # -------------------------------------------------
        # 11. WAIT FOR LESION DETAILS FORM
        # -------------------------------------------------

        print("\nWaiting for lesion details form...")

        age_field = WebDriverWait(
            driver, 30
        ).until(
            EC.visibility_of_element_located(
                (
                    AppiumBy.XPATH,
                    "//android.widget.EditText[@index='6']"
                )
            )
        )

        print("Lesion details form opened.")

        # -------------------------------------------------
        # 12. ENTER AGE
        # -------------------------------------------------

        age_field.click()
        age_field.clear()

        driver.set_clipboard_text(PATIENT_AGE)
        age_field.click()
        driver.press_keycode(279)

        print(f"Age entered: {PATIENT_AGE}")

        # -------------------------------------------------
        # 13. SELECT SEX
        # -------------------------------------------------

        sex_dropdown = wait.until(
            EC.element_to_be_clickable(
                (
                    AppiumBy.XPATH,
                    "//*[@text='—']"
                )
            )
        )
        sex_dropdown.click()

        female_option = wait.until(
            EC.element_to_be_clickable(
                (
                    AppiumBy.XPATH,
                    "//*[@text='Female']"
                )
            )
        )
        female_option.click()

        print(f"{PATIENT_SEX} selected.")

        # -------------------------------------------------
        # 14. ENTER DURATION DIRECTLY
        # NO BODY-MAP / LESION-LOCATION SELECTION
        # -------------------------------------------------

        print("\nEntering lesion duration directly...")

        duration = wait.until(
            EC.visibility_of_element_located(
                (
                    AppiumBy.XPATH,
                    "//android.widget.EditText"
                    "[@hint='e.g. 3 months, growing']"
                )
            )
        )

        duration.click()
        duration.clear()
        duration.send_keys(LESION_DURATION)

        print(f"Duration entered: {LESION_DURATION}")

        # -------------------------------------------------
        # 15. HIDE KEYBOARD
        # -------------------------------------------------

        try:
            driver.hide_keyboard()
            print("Keyboard hidden.")
        except Exception:
            print("Keyboard already hidden.")

        # -------------------------------------------------
        # 16. TAP ANALYZE
        # -------------------------------------------------

        analyze_button = wait.until(
            EC.element_to_be_clickable(
                (
                    AppiumBy.XPATH,
                    "//android.widget.Button"
                    "[@text='Analyze & generate report']"
                )
            )
        )

        analyze_button.click()

        print("Analyze & generate report clicked.")

        # -------------------------------------------------
        # 17. WAIT FOR AI ANALYSIS UP TO 120 SECONDS
        # -------------------------------------------------

        report_text = wait_for_ai_report(
            driver,
            timeout=120
        )

        print("\n========== INITIAL REPORT ==========")
        print(report_text[:6000])
        print("========== END INITIAL REPORT ==========")

        # -------------------------------------------------
        # 18. INSPECT TREATMENT SECTIONS
        # -------------------------------------------------

        scroll_report(driver)
        report_text = get_report_text(driver)
        report_lower = report_text.lower()

        allopathic_present = (
            "allopathic" in report_lower
            or "allopathy treatment" in report_lower
        )

        ayurveda_present = (
            "ayurveda" in report_lower
            or "ayurvedic" in report_lower
        )

        first_line_present = "first line" in report_lower
        barrier_present = "barrier" in report_lower

        empty_first_line = (
            "first line: —" in report_lower
            or "first line: -" in report_lower
        )

        print("\n========== REPORT VALIDATION ==========")
        print(f"Allopathic section found: {allopathic_present}")
        print(f"Ayurveda section found: {ayurveda_present}")
        print(f"First line text found: {first_line_present}")
        print(f"Empty first-line treatment: {empty_first_line}")
        print(f"Barrier text found: {barrier_present}")

        # -------------------------------------------------
        # 19. DETECT KNOWN APPLICATION DEFECT
        # -------------------------------------------------

        treatment_missing = (
            not allopathic_present
            and not ayurveda_present
            and not barrier_present
        )

        bug_detected = treatment_missing or empty_first_line

        if bug_detected:
            screenshot_path = os.path.join(
                SCREENSHOT_DIR,
                "GPD-07-treatment-bug.png"
            )

            driver.save_screenshot(screenshot_path)

            print(f"\n{BUG_ID} reproduced.")
            print(f"Screenshot saved: {screenshot_path}")

            # Jira reporting is optional for test execution.
            # The helper should read Priority/Severity from Excel.
            try:
                from utils.bug_reporter import report_bug_to_jira

                print("\nSending defect details to Jira...")

                report_bug_to_jira(
                    driver=driver,
                    test_case_id="GPD-07",
                    bug_title=(
                        "Treatment recommendations are not "
                        "populated in targeted lesion report"
                    ),
                    actual_result=(
                        "The AI report was generated, but the "
                        "required treatment recommendations and/or "
                        "barrier repair regimen were missing or "
                        "the first-line treatment was empty."
                    ),
                    expected_result=(
                        "The report should display the expected "
                        "treatment recommendations and barrier "
                        "repair regimen."
                    ),
                    screenshot_path=screenshot_path
                )

                print("Jira reporting completed.")

            except Exception as error:
                print(f"Jira reporting failed: {error}")
                print(
                    "Preserving the original pytest result."
                )

            pytest.fail(
                f"{BUG_ID}: Expected treatment recommendations "
                "or barrier repair information were not populated."
            )

        # -------------------------------------------------
        # 20. TEST PASSED
        # -------------------------------------------------

        print("\n========================================")
        print("GPD-07 PASSED")
        print("========================================")
        print("AI report generated and treatment content detected.")

    except Exception:
        screenshot_path = os.path.join(
            SCREENSHOT_DIR,
            "GPD-07-failure.png"
        )

        os.makedirs(SCREENSHOT_DIR, exist_ok=True)

        try:
            driver.save_screenshot(screenshot_path)
            print(f"Failure screenshot saved: {screenshot_path}")
        except Exception:
            pass

        raise
