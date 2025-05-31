import sys
import os
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from context_memory import get_context
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatLiteLLM
from langchain.chains import LLMChain
from action_executor import execute_action

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
- If you're not sure, suggest asking the user to clarify.

Respond in this JSON format:
{{
  "action": "create_ticket" | "update_ticket" | "clarify",
  "reason": "...",
  "summary": "...",
  "target_issue_key": "...",
  "comment": "...",
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

    import litellm
    litellm._turn_on_debug()

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
            "assignee": context.get("default_assignee") or "Unassigned"
        }

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
    test_notes = "We need to fix the login issue again, users are stuck on Safari."
    final_result = sidekick_core(test_notes)
    print("\n🎯 Final Outcome:", final_result)
