import os
from datetime import datetime

from .jira_client import JiraClient
from config.test_case_metadata import get_test_metadata

def report_bug_to_jira(driver, test_case_id, bug_title, actual_result, expected_result, screenshot_path):
    """
    Reports a bug to Jira. Looks up metadata from Excel dynamically.
    Checks for duplicates, adds a comment if found, creates a new one otherwise.
    Attaches screenshot.
    """
    try:
        # 1. Capture screenshot if not already captured.
        if not os.path.exists(screenshot_path):
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            driver.save_screenshot(screenshot_path)
            
        # 2. Get Metadata
        metadata = get_test_metadata(test_case_id)
        priority = metadata.get("priority", "P2 - Medium")
        severity = metadata.get("severity", "Medium")
        module = metadata.get("module", "GP-Derma")
        feature = metadata.get("feature", "")
        scenario = metadata.get("scenario", "")
        preconditions = metadata.get("preconditions", "")
        steps = metadata.get("steps", "")
        tester_notes = metadata.get("tester_notes", "")
        if not expected_result:
            expected_result = metadata.get("expected_result", "")
            
        jira = JiraClient()
        
        # Determine exact summary to look for
        full_summary = f"[{test_case_id}] {bug_title}"
        
        print("\n========================================")
        print("JIRA BUG REPORT")
        print("========================================")
        print(f"Test Case: {test_case_id}")
        print(f"Priority: {priority}")
        print(f"Severity: {severity}")
        print("Environment: GP-Derma Development")
        print("Reporter: Divya")
        print(f"\nBug detected:\n{bug_title}")
        
        # 3. Look for existing matching Jira bug
        existing_issue = jira.find_existing_bug(test_case_id, bug_title)
        
        issue_key = None
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if existing_issue:
            issue_key = existing_issue["key"]
            print(f"\nExisting Jira bug found:\n{issue_key}")
            print("No duplicate issue created.")
            
            # Add comment with latest execution info
            comment = (
                f"Automation test run on {timestamp} reproduced this bug.\n"
                f"Actual Result observed:\n{actual_result}"
            )
            jira.add_comment(issue_key, comment)
            
            # Attach latest screenshot
            if jira.attach_screenshot(issue_key, screenshot_path):
                print("Latest screenshot attached.")
            else:
                print("Failed to attach latest screenshot.")
        else:
            print("\nCreating Jira issue...")
            # 4. Create a new Jira bug if necessary
            description = f"""Bug detected during automated GP-Derma Android testing.

*Test Case ID:*
{test_case_id}

*Module:*
{module}

*Feature / Screen:*
{feature}

*Environment:*
GP-Derma Development

*Priority:*
{priority}

*Severity:*
{severity}

*Reporter:*
Divya

*Test Scenario:*
{scenario}

*Pre-Conditions:*
{preconditions}

*Steps to Reproduce:*
{steps}

*Expected Result:*
{expected_result}

*Actual Result:*
{actual_result}

*Tester Notes:*
{tester_notes}

*Automation Result:*
FAILED / BUG DETECTED

*Timestamp:*
{timestamp}
"""
            issue_key = jira.create_bug(
                summary=full_summary,
                description=description,
                priority=priority
            )
            print(f"\nJira issue created:\n{issue_key}")
            
            # 5. Attach screenshot
            if jira.attach_screenshot(issue_key, screenshot_path):
                print(f"Screenshot attached:\n{screenshot_path}")
            else:
                print("Failed to attach screenshot.")
                
        # Print URL
        if issue_key and jira.base_url:
            print(f"\nJira URL:\n{jira.base_url}/browse/{issue_key}")
            
        print("========================================")
        return issue_key
    
    except Exception as e:
        print(f"\nJira reporting failed: {e}\nContinuing with pytest failure...")
        return None
