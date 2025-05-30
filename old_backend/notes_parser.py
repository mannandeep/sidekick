import os
import json
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

load_dotenv()

# Load model
provider = os.getenv("LLM_PROVIDER", "openai")

if provider == "lmstudio":
    llm = ChatOpenAI(
        temperature=0,
        model="mistral-7b-instruct-v0.1",
        openai_api_base="http://localhost:1234/v1",
        openai_api_key="sk-anything"
    )
else:
    llm = ChatOpenAI(
        temperature=0,
        model="gpt-4",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

# Smart Prompt: Decide what to create from messy notes
NOTES_PARSER_PROMPT = PromptTemplate(
    input_variables=["notes"],
    template="""
You are a smart product assistant. Your job is to read messy product or engineering notes and extract a list of clear, structured Jira tasks.

Instructions:
- Read the notes carefully and break them into actionable work items.
- For each item, return a JSON object with the following fields:
  - title: A short, clear summary of the task (max 1 line)
  - description: 1–3 lines explaining what needs to be done and why
  - ticket_type: One of ['Bug', 'Story', 'Task', 'Epic', 'Project']
  - priority: One of ['Low', 'Medium', 'High'] — use only if it's implied
  - due_date: In YYYY-MM-DD format, if any deadline is mentioned
  - assignee: Name or email of the person responsible, if mentioned

Only include fields that are clearly mentioned or strongly implied.

Respond ONLY with a JSON array of items like this:
[
  {{
    "title": "Fix login redirect issue",
    "description": "Safari users are redirected incorrectly after login. Needs investigation and patch.",
    "ticket_type": "Bug",
    "priority": "High",
    "due_date": "2025-06-01",
    "assignee": "amit@company.com"
  }},
  ...
]

Input Notes:
{notes}
"""
)


notes_parser_chain = LLMChain(llm=llm, prompt=NOTES_PARSER_PROMPT)

def parse_notes_into_jira_tasks(notes: str) -> list:
    response = notes_parser_chain.run(notes=notes)
    try:
        return json.loads(response)
    except Exception as e:
        print("❌ Failed to parse model response:", e)
        print("Raw model output:", response)
        return []
