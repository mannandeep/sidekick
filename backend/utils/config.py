import os

REQUIRED_VARS = ["JIRA_URL", "JIRA_EMAIL", "JIRA_API_TOKEN", "JIRA_DOMAIN"]

def require_env_vars(vars=REQUIRED_VARS):
    missing = [v for v in vars if not os.getenv(v)]
    if missing:
        raise EnvironmentError(
            "Missing required environment variables: " + ", ".join(missing)
        )
