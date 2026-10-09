import time

from appium.webdriver.common.appiumby import AppiumBy


# ============================================================
# HELPER: GET VISIBLE TEXT
# ============================================================

def get_visible_text(driver):

    texts = []

    try:

        elements = driver.find_elements(
            AppiumBy.XPATH,
            "//*[@text]"
        )

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


# ============================================================
# HELPER: FIND PATIENT SEARCH FIELD
# ============================================================

def find_patient_search(driver, timeout=30):

    end_time = time.time() + timeout

    while time.time() < end_time:

        try:

            fields = driver.find_elements(
                AppiumBy.XPATH,
                "//android.widget.EditText"
                "[@hint='Search by name or phone']"
            )

            for field in fields:

                try:

                    if field.is_displayed():
                        return field

                except Exception:
                    pass

        except Exception:
            pass

        time.sleep(1)

    return None


# ============================================================
# GPD-11
# Patient Roster & History
# ============================================================

def test_gpd_11_patient_roster_and_history(
    logged_in_driver
):

    driver = logged_in_driver

    try:

        print(
            "\n========================================"
        )
        print(
            "GPD-11: Patient Roster & History"
        )
        print(
            "========================================"
        )

        # ========================================================
        # 1. LOGIN
        # ========================================================

        print(
            "\nLogin completed successfully."
        )

        time.sleep(2)

        # ========================================================
        # 2. SCROLL HOME SCREEN
        # ========================================================

        print(
            "\nScrolling Recent Scans down..."
        )

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

        print(
            "Home screen scrolled."
        )

        # ========================================================
        # 3. OPEN PATIENTS
        # ========================================================

        print(
            "\nOpening Patients..."
        )

        # Patients bottom navigation
        # Inspector bounds:
        # [378,2270][433,2325]
        #
        # Center:
        # (405,2297)

        driver.execute_script(
            "mobile: clickGesture",
            {
                "x": 405,
                "y": 2297
            }
        )

        print(
            "Patients clicked."
        )

        time.sleep(4)

        # ========================================================
        # 4. WAIT FOR SEARCH FIELD
        # ========================================================

        print(
            "\nWaiting for Patients search field..."
        )

        search = find_patient_search(
            driver,
            timeout=30
        )

        if search is None:

            print(
                "\n========== CURRENT SCREEN =========="
            )

            print(
                get_visible_text(driver)
            )

            print(
                "========== END CURRENT SCREEN =========="
            )

            driver.save_screenshot(
                "screenshots/GPD-11-search-failure.png"
            )

            raise AssertionError(
                "Patients search field was not found."
            )

        print(
            "Patients search field found."
        )

        # ========================================================
        # 5. ENTER ONLY "ARUN SHARMA"
        # ========================================================

        print(
            "\nEntering patient name..."
        )

        search.click()

        time.sleep(0.5)

        try:
            search.clear()
        except Exception:
            pass

        time.sleep(0.5)

        # ONLY THIS TEXT
        search.send_keys(
            "Arun Sharma"
        )

        print(
            "Search text entered: Arun Sharma"
        )

        # Wait for records
        time.sleep(3)

        # ========================================================
        # 6. VERIFY PATIENT RECORDS ARE DISPLAYED
        # ========================================================

        print(
            "\nChecking Arun Sharma records..."
        )

        end_time = time.time() + 30

        patient_cards = []

        while time.time() < end_time:

            try:

                cards = driver.find_elements(
                    AppiumBy.XPATH,
                    "//android.widget.Button"
                    "[contains(@text,'Arun Sharma')]"
                )

                patient_cards = []

                for card in cards:

                    try:

                        if (
                            card.is_displayed()
                            and
                            card.is_enabled()
                        ):

                            patient_cards.append(
                                card
                            )

                    except Exception:
                        pass

                if patient_cards:
                    break

            except Exception:
                pass

            time.sleep(1)

        # ========================================================
        # 7. RECORDS NOT FOUND
        # ========================================================

        if not patient_cards:

            print(
                "\n========== CURRENT SCREEN =========="
            )

            print(
                get_visible_text(driver)
            )

            print(
                "========== END CURRENT SCREEN =========="
            )

            driver.save_screenshot(
                "screenshots/GPD-11-records-not-found.png"
            )

            raise AssertionError(
                "No Arun Sharma patient records were displayed."
            )

        # ========================================================
        # 8. PRINT DISPLAYED RECORDS
        # ========================================================

        print(
            f"\nArun Sharma records displayed: "
            f"{len(patient_cards)}"
        )

        for index, card in enumerate(
            patient_cards,
            start=1
        ):

            print(
                f"Record {index}: {card.text}"
            )

        # ========================================================
        # 9. FINAL VALIDATION
        # ========================================================

        screen = get_visible_text(
            driver
        )

        assert "Arun Sharma" in screen, (
            "Arun Sharma was not displayed "
            "in the search results."
        )

        print(
            "\n✓ Search: Arun Sharma"
        )

        print(
            "✓ Patient records displayed"
        )

        print(
            "\n========================================"
        )

        print(
            "GPD-11 PASSED"
        )

        print(
            "========================================"
        )

        print(
            "Test completed after displaying "
            "Arun Sharma patient records."
        )

        print(
            "========================================"
        )

    except Exception:

        try:

            driver.save_screenshot(
                "screenshots/GPD-11-failure.png"
            )

            print(
                "\nFailure screenshot saved:"
            )

            print(
                "screenshots/GPD-11-failure.png"
            )

        except Exception:
            pass

        raise