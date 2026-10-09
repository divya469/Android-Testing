import os
import requests
from requests.auth import HTTPBasicAuth

class JiraClient:
    def __init__(self):
        self.base_url = os.environ.get("JIRA_URL")
        self.email = os.environ.get("JIRA_EMAIL")
        self.api_token = os.environ.get("JIRA_API_TOKEN")
        self.project_key = os.environ.get("JIRA_PROJECT_KEY", "AT")
        
        if not all([self.base_url, self.email, self.api_token]):
            print("WARNING: Jira credentials missing in environment variables.")
            
        self.auth = HTTPBasicAuth(self.email, self.api_token) if self.email and self.api_token else None

    def find_existing_bug(self, test_case_id, summary):
        if not self.auth:
            return None
        
        # Searching by a unique prefix or exact title
        # "summary ~" does a text search. Let's make sure it matches the exact summary part.
        summary_query = f"[{test_case_id}] {summary}"
        jql = f'project = {self.project_key} AND summary ~ "\\"{summary_query}\\"" AND statusCategory != Done ORDER BY created DESC'
        url = f"{self.base_url}/rest/api/3/search/jql"
        
        try:
            response = requests.post(
                url,
                headers={"Accept": "application/json", "Content-Type": "application/json"},
                json={"jql": jql, "maxResults": 1},
                auth=self.auth,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            if data.get("issues") and len(data["issues"]) > 0:
                # Jira's text search might return partial matches, so verify exact match if needed.
                return data["issues"][0]
        except Exception as e:
            print(f"Failed to search existing Jira issue: {e}")
            if hasattr(e, "response") and e.response is not None:
                print(f"Response: {e.response.text}")
        return None

    def create_bug(self, summary, description, priority="P2 - Medium"):
        if not self.auth:
            raise Exception("Jira authentication not configured.")
            
        url = f"{self.base_url}/rest/api/2/issue"
        
        # Determine Jira Priority id or name
        jira_priority = "Medium"
        if "P0" in priority:
            jira_priority = "Highest"
        elif "P1" in priority:
            jira_priority = "High"
        elif "P3" in priority:
            jira_priority = "Low"
            
        payload = {
            "fields": {
                "project": {
                    "key": self.project_key
                },
                "summary": summary,
                "description": description,
                "issuetype": {
                    "name": "Bug"
                },
                "priority": {
                    "name": jira_priority
                }
            }
        }
        
        response = requests.post(
            url,
            json=payload,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            auth=self.auth,
            timeout=10
        )
        
        if response.status_code == 201:
            return response.json()["key"]
        else:
            raise Exception(f"Failed to create Jira issue: {response.text}")

    def add_comment(self, issue_key, comment_text):
        if not self.auth:
            return
            
        url = f"{self.base_url}/rest/api/2/issue/{issue_key}/comment"
        payload = {
            "body": comment_text
        }
        
        try:
            response = requests.post(
                url,
                json=payload,
                headers={"Accept": "application/json", "Content-Type": "application/json"},
                auth=self.auth,
                timeout=10
            )
            response.raise_for_status()
        except Exception as e:
            print(f"Failed to add comment to {issue_key}: {e}")

    def attach_screenshot(self, issue_key, file_path):
        if not self.auth:
            return False
            
        if not os.path.exists(file_path):
            print(f"Screenshot not found at {file_path}")
            return False
            
        url = f"{self.base_url}/rest/api/2/issue/{issue_key}/attachments"
        headers = {
            "Accept": "application/json",
            "X-Atlassian-Token": "no-check"
        }
        
        try:
            with open(file_path, "rb") as f:
                files = {
                    "file": (os.path.basename(file_path), f, "image/png")
                }
                response = requests.post(
                    url,
                    headers=headers,
                    files=files,
                    auth=self.auth,
                    timeout=20
                )
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Failed to attach file to {issue_key}: {e}")
            return False
