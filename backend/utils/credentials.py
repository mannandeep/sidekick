import os
import json
from pathlib import Path

CREDS_PATH = Path(__file__).resolve().parent.parent / "jira_credentials.json"


def load_credentials():
    """Load Jira credentials from env vars or stored file."""
    url = os.getenv("JIRA_URL")
    email = os.getenv("JIRA_EMAIL")
    token = os.getenv("JIRA_API_TOKEN")
    domain = os.getenv("JIRA_DOMAIN")

    if all([url, email, token, domain]):
        return {
            "url": url,
            "email": email,
            "api_token": token,
            "domain": domain,
        }

    if CREDS_PATH.exists():
        with open(CREDS_PATH) as f:
            data = json.load(f)
            return data
    return None


def save_credentials(url: str, email: str, api_token: str, domain: str) -> None:
    CREDS_PATH.write_text(
        json.dumps(
            {
                "url": url,
                "email": email,
                "api_token": api_token,
                "domain": domain,
            },
            indent=2,
        )
    )
