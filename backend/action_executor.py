from jira_utils import create_ticket, update_ticket
from prd_generator import generate_prd

def execute_action(decision: dict):
    action = decision.get("action")
    print(f"\n⚙️ Action to perform: {action}")

    if action == "create_ticket":
        return create_ticket(
            summary=decision.get("summary"),
            description=decision.get("reason"),
            assignee=decision.get("assignee")
        )

    elif action == "update_ticket":
        return update_ticket(
            issue_key=decision.get("target_issue_key"),
            comment=decision.get("comment")
        )

    elif action == "generate_prd":
        return generate_prd(summary=decision.get("summary"))

    elif action == "clarify":
        return "🤔 Agent needs clarification from the user."

    elif action == "gather_info":
        print("\n🤔 Sidekick needs more information before proceeding:")
        for i, q in enumerate(decision.get("questions", []), 1):
            print(f"  {i}. {q}")
        return {"status": "follow_up_needed", "questions": decision.get("questions", [])}

    else:
        return f"🚫 Unknown action type: {action}"
