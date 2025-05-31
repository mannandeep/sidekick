import json
from jira_utils import create_ticket, update_ticket


def execute_action(decision: dict):
    action = decision.get("action")

    if action == "create_ticket":
        print("\n🚀 Creating a new Jira ticket...")
        issue_key = create_ticket(
            project_key=decision.get("project_key"),
            summary=decision.get("summary"),
            description=decision.get("reason"),
            assignee=decision.get("assignee")
        )
        return {"status": "created", "issue_key": issue_key}

    elif action == "update_ticket":
        print(f"\n🔄 Updating existing issue: {decision.get('target_issue_key')}")
        updated_key = update_ticket(
            issue_key=decision.get("target_issue_key"),
            comment=decision.get("comment")
        )
        return {"status": "updated", "issue_key": updated_key}

    elif action == "clarify":
        print("\n❓ LLM was not confident enough to take an action.")
        print("📣 It suggested clarification:\n", decision.get("reason"))
        return {"status": "clarify", "message": decision.get("reason")}

    else:
        print("\n❌ Unknown action type. No action taken.")
        return {"status": "error", "message": "Unrecognized action."}
