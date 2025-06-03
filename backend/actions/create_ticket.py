from ..jira.jira_utils import create_ticket
from ..context.context_memory import get_context


def run(summary: str, description: str, assignee: str | None):
    """Create a Jira ticket in the active project."""
    context = get_context()
    project_key = context.get("active_project_key")
    if not project_key:
        return "No active project configured."
    return create_ticket(project_key, summary, description, assignee)
