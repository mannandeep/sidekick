from ..jira.jira_utils import update_ticket


def run(issue_key: str, comment: str):
    """Update a Jira ticket with a comment."""
    return update_ticket(issue_key, comment)
