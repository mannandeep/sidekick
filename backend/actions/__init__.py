from .create_ticket import run as create_ticket_action
from .update_ticket import run as update_ticket_action
from .generate_prd import run as generate_prd_action
from .clarify import run as clarify_action
from .gather_info import run as gather_info_action


def execute_action(decision: dict):
    action = decision.get("action")
    print(f"\n⚙️ Action to perform: {action}")

    if action == "create_ticket":
        return create_ticket_action(
            summary=decision.get("summary"),
            description=decision.get("reason"),
            assignee=decision.get("assignee"),
        )
    elif action == "update_ticket":
        return update_ticket_action(
            issue_key=decision.get("target_issue_key"),
            comment=decision.get("comment"),
        )
    elif action == "generate_prd":
        return generate_prd_action(summary=decision.get("summary"))
    elif action == "clarify":
        return clarify_action()
    elif action == "gather_info":
        return gather_info_action(decision.get("questions", []))
    else:
        return f"🚫 Unknown action type: {action}"
