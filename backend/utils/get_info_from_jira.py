import json
import os
from pathlib import Path
import requests
from dotenv import load_dotenv

load_dotenv()

JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
JIRA_HEADERS = { "Accept": "application/json" }
JIRA_AUTH = (JIRA_EMAIL, JIRA_API_TOKEN)

def get_all_projects():
    url = f"https://{JIRA_DOMAIN}/rest/api/3/project"
    response = requests.get(url, headers=JIRA_HEADERS, auth=JIRA_AUTH)
    if response.status_code == 200:
        return response.json()
    print(f"❌ Project fetch failed: {response.status_code} - {response.text}")
    return []

def get_issues_for_project(project_key, max_results=100):
    url = f"https://{JIRA_DOMAIN}/rest/api/3/search"
    params = {
        "jql": f"project={project_key}",
        "maxResults": max_results
    }
    response = requests.get(url, headers=JIRA_HEADERS, auth=JIRA_AUTH, params=params)
    if response.status_code == 200:
        return response.json().get("issues", [])
    print(f"❌ Issue fetch failed for {project_key}: {response.status_code} - {response.text}")
    return []

def get_comments(issue_key):
    url = f"https://{JIRA_DOMAIN}/rest/api/3/issue/{issue_key}/comment"
    response = requests.get(url, headers=JIRA_HEADERS, auth=JIRA_AUTH)
    if response.status_code == 200:
        return response.json().get("comments", [])
    return []

def build_full_snapshot():
    snapshot = { "projects": [] }
    projects = get_all_projects()
    for proj in projects:
        proj_data = {
            "id": proj.get("id"),
            "key": proj.get("key"),
            "name": proj.get("name"),
            "issues": []
        }
        issues = get_issues_for_project(proj["key"])
        for issue in issues:
            fields = issue.get("fields", {})
            issue_data = {
                "key": issue.get("key"),
                "summary": fields.get("summary"),
                "status": fields.get("status", {}).get("name"),
                "assignee": (fields.get("assignee") or {}).get("displayName"),
                "updated": fields.get("updated"),
                "comments": get_comments(issue.get("key"))
            }
            proj_data["issues"].append(issue_data)
        snapshot["projects"].append(proj_data)
    return snapshot

def save_snapshot(snapshot, filename: str | None = None):
    if filename is None:
        filename = Path(__file__).parent.parent / "jira_memory.json"
    else:
        filename = Path(filename)
    with open(filename, "w") as f:
        json.dump(snapshot, f, indent=2)
    print(f"✅ Jira snapshot saved to {filename}")

if __name__ == "__main__":
    print("📡 Building full Jira memory snapshot...")
    snapshot = build_full_snapshot()
    save_snapshot(snapshot)
