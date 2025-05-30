import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from context_memory import get_context
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatLiteLLM

# Load vectorstore
def load_vectorstore(index_path="faiss_index"):
    embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local(index_path, embeddings=embedding, allow_dangerous_deserialization=True)
    return vectorstore

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
    #llm = ChatOpenAI(temperature=0.2)

    from langchain_community.chat_models import ChatLiteLLM

    llm = ChatLiteLLM(
        model="custom/mistral",  # ✅ 'custom/' prefix is needed
        api_base="http://localhost:1234/v1",  # ✅ LM Studio API
        api_key="not-needed",  # ✅ Dummy key
        litellm_provider="custom",  # ✅ Use 'custom'
        custom_llm_provider="custom",  # ✅ Must match the prefix
        model_alias="mistral",  # Optional: name used in logs
        temperature=0.2
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    joined_issues = "\n\n".join(similar_issues)
    response = chain.run({
        "notes": notes,
        "project_key": context.get("active_project_key"),
        "assignee": context.get("default_assignee") or "Unassigned",
        "similar_issues": joined_issues
    })

    import json

    print("\n🧠 Agent's Reasoning Output:\n", response)

    # Try to parse the response into JSON
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

    return decision


# Core Sidekick function
def sidekick_core(notes: str):
    # Step 1: Get context
    context = get_context()
    project_key = context.get("active_project_key") or "❓ Not set"
    assignee = context.get("default_assignee") or "Unassigned"

    print("🧠 Running Sidekick Core...")
    print(f"📄 Notes: {notes}")
    print(f"📂 Active Project: {project_key}")
    print(f"👤 Default Assignee: {assignee}")

    # Step 2: Run RAG search on the notes
    vectorstore = load_vectorstore()
    similar_issues = vectorstore.similarity_search(notes, k=3)

    print("\n🔎 Top Similar Issues from Memory:")
    for i, doc in enumerate(similar_issues, 1):
        print(f"\nResult {i}:\n{doc.page_content}\n{'-'*40}")

    # Step 3: (Next Step) → Build prompt for reasoning

    return run_decision_chain(notes, context, [doc.page_content for doc in similar_issues])


if __name__ == "__main__":
    test_notes = "We need to fix the login issue again, users are stuck on Safari."
    sidekick_core(test_notes)
