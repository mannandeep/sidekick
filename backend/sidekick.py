import json

from .context.context_memory import get_context
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatLiteLLM
from langchain.chains import LLMChain
from .actions import execute_action

# Load vectorstore
def load_vectorstore(index_path="faiss_index"):
    embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local(index_path, embeddings=embedding, allow_dangerous_deserialization=True)
    return vectorstore

# Run LLM reasoning + execute action
def run_decision_chain(notes, context, similar_issues):
    template = """
You are Sidekick, an AI assistant for product managers.

Here are the user’s notes:
"{notes}"

Here is the active context:
- Project Key: {project_key}
- Default Assignee: {assignee}

Here are similar past issues from memory:
{similar_issues}

---

Think carefully:
- If this looks like a new issue, suggest creating a ticket.
- If it's similar to an existing issue, suggest updating or commenting on it.
- If the user is requesting a structured document like a PRD, choose "generate_prd" as the action.
- If you need more information to proceed, ask the user for it by returning `gather_info` and listing your questions.
- If you're not sure, suggest asking the user to clarify.

Respond in this JSON format:
{{
  "action": "create_ticket" | "update_ticket" | "clarify" | "gather_info" | "generate_prd",
  "reason": "...",
  "summary": "...",
  "target_issue_key": "...",
  "comment": "...",
  "questions": ["...","..."],
  "assignee": "{assignee}"
}}
"""

    prompt = PromptTemplate.from_template(template)

    llm = ChatLiteLLM(
        model="mistral",
        api_base="http://localhost:1234/v1",
        api_key="not-needed",
        custom_llm_provider="openai"
    )

    chain = LLMChain(llm=llm, prompt=prompt)
    joined_issues = "\n\n".join(similar_issues)
    response = chain.run({
        "notes": notes,
        "project_key": context.get("active_project_key"),
        "assignee": context.get("default_assignee") or "Unassigned",
        "similar_issues": joined_issues
    })

    print("\n🧠 Agent's Reasoning Output:\n", response)

    try:
        try:
            decision = json.loads(response)
        except json.JSONDecodeError:
            response = response.strip().replace("None", "null")
            decision = json.loads(response)

        print("\n✅ Parsed Decision:\n", json.dumps(decision, indent=2))
    except json.JSONDecodeError:
        print("❌ Could not parse response as JSON.")
        decision = {
            "action": "clarify",
            "reason": "LLM response could not be parsed.",
            "summary": "",
            "target_issue_key": "",
            "comment": "",
            "questions": [],
            "assignee": context.get("default_assignee") or "Unassigned"
        }

    # Execute the action and return result
    print("\n⚙️ Executing the suggested action...")
    result = execute_action(decision)
    print("\n📬 Action result:", result)
    return result


# Core function
def sidekick_core(notes: str):
    context = get_context()
    project_key = context.get("active_project_key") or "❓ Not set"
    assignee = context.get("default_assignee") or "Unassigned"

    print("🧠 Running Sidekick Core...")
    print(f"📄 Notes: {notes}")
    print(f"📂 Active Project: {project_key}")
    print(f"👤 Default Assignee: {assignee}")

    vectorstore = load_vectorstore()
    similar_issues = vectorstore.similarity_search(notes, k=3)

    print("\n🔎 Top Similar Issues from Memory:")
    for i, doc in enumerate(similar_issues, 1):
        print(f"\nResult {i}:\n{doc.page_content}\n{'-'*40}")

    return run_decision_chain(notes, context, [doc.page_content for doc in similar_issues])

# Run directly
if __name__ == "__main__":
    test_notes = """
    We’re planning to build a new onboarding flow for first-time users in our web app. The goal is to help new users understand the product faster and get to their first meaningful action within 2 minutes.

    Here’s what we know:
    - Target users: Early-stage startup founders using our analytics dashboard
    - Pain point: They sign up but don’t understand how to connect their data or what metrics to focus on
    - Current drop-off: 68% of new users leave before completing setup
    - Hypothesis: If we guide them through setting up their first workspace and help them see dummy data, they’ll understand the value faster
    - Inspiration: Figma's collaborative onboarding + Notion’s quickstart templates

    Can you create a complete PRD for this feature?

    It should include:
    - Background and problem
    - Goals and success metrics
    - User stories
    - Milestones
    - Team
    - Open questions

    Assume this is part of our core product team’s Q3 priorities.
    """

    final_result = sidekick_core(test_notes)
    print("\n🎯 Final Outcome:", final_result)
