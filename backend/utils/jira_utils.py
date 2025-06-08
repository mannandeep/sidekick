import os
from dotenv import load_dotenv
from jira import JIRA
from .credentials import load_credentials

load_dotenv()
creds = load_credentials()
if not creds:
    raise EnvironmentError(
        "Jira credentials not provided. Set env vars or use /connect_jira endpoint."
    )

JIRA_URL = creds["url"]
JIRA_EMAIL = creds["email"]
JIRA_API_TOKEN = creds["api_token"]

jira = JIRA(
    server=JIRA_URL,
    basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN)
)


def create_ticket(project_key: str, summary: str, description: str, assignee: str = None) -> str:
    issue_dict = {
        'project': {'key': project_key},
        'summary': summary,
        'description': description,
        'issuetype': {'name': 'Task'}
    }
    if assignee:
        issue_dict['assignee'] = {'name': assignee}

    issue = jira.create_issue(fields=issue_dict)
    print(f"✅ Created ticket: {issue.key}")
    return issue.key


def update_ticket(issue_key: str, comment: str) -> str:
    issue = jira.issue(issue_key)
    jira.add_comment(issue, comment)
    print(f"📝 Added comment to {issue_key}")
    return issue_key


def comment_on_ticket(issue_key: str, comment: str):
    jira.add_comment(issue_key, comment)
    print(f"💬 Commented on {issue_key}")
