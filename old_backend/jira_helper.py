import os
import requests
from dotenv import load_dotenv

load_dotenv()

JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")
JIRA_ACCOUNT_ID = os.getenv("JIRA_ACCOUNT_ID")

def create_jira_ticket(title, description, issue_type="Task", priority=None, assignee_id=None, due_date=None):
    url = f"https://{JIRA_DOMAIN}/rest/api/3/issue"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    auth = (JIRA_EMAIL, JIRA_API_TOKEN)

    fields = {
        "project": { "key": JIRA_PROJECT_KEY },
        "summary": title,
        "description": {
            "type": "doc",
            "version": 1,
            "content": [{
                "type": "paragraph",
                "content": [{
                    "text": description,
                    "type": "text"
                }]
            }]
        },
        "issuetype": { "name": issue_type }
    }

    if priority:
        fields["priority"] = { "name": priority }

    if assignee_id:
        fields["assignee"] = { "id": assignee_id }

    if due_date:
        fields["duedate"] = due_date

    response = requests.post(url, json={ "fields": fields }, headers=headers, auth=auth)

    if response.status_code == 201:
        print(f"✅ Created ticket: {title}")
        return response.json()
    else:
        print(f"❌ Failed to create ticket: {response.status_code} - {response.text}")
        return None

def create_jira_project(project_name: str, project_key: str = "AI1") -> dict:
    url = f"https://{JIRA_DOMAIN}/rest/api/3/project"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {
        "key": project_key,
        "name": project_name,
        "projectTypeKey": "software",
        "projectTemplateKey": "com.pyxis.greenhopper.jira:gh-scrum-template",
        "description": "Created by Sidekick AI",
        "leadAccountId": JIRA_ACCOUNT_ID,
        "assigneeType": "PROJECT_LEAD"
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        return response.json()
    else:
        print("❌ Failed to create project:", response.status_code, response.text)
        return {}
