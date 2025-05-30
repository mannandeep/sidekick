import os
import json
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType

from notes_parser import parse_notes_into_jira_tasks
from jira_helper import create_jira_ticket, create_jira_project

load_dotenv()

# 🔐 Load model
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

# 🧠 Dummy map: name/email → Jira account ID
ASSIGNEE_MAP = {
    "amit": "1234567890abcdefamitid",
    "amit@company.com": "1234567890abcdefamitid",
    "aditi": "123aditi09876xyzid",
    "prashant": "prashantabcid123"
}

def lookup_account_id(assignee_field):
    if not assignee_field:
        return None
    key = assignee_field.strip().lower()
    return ASSIGNEE_MAP.get(key)

# 🛠️ Tool 1: Create Jira Project (wrapped to accept one str input)
def create_project_tool(raw_input: str) -> str:
    try:
        project_name = raw_input.strip()
        if raw_input.startswith("{"):
            parsed = json.loads(raw_input)
            project_name = parsed.get("project_name", project_name)
        key = "".join([c for c in project_name.upper() if c.isalpha()])[:4]
        result = create_jira_project(project_name, project_key=key)
        if result:
            return f"✅ Created Jira project '{project_name}' with key {key}"
        return "❌ Project creation failed."
    except Exception as e:
        return f"❌ Error in create_project_tool: {str(e)}"

# 🛠️ Tool 2: Full Notes → Parse → Create Tickets
def full_notes_to_jira(raw_input: str) -> str:
    try:
        notes = raw_input.strip()
        tasks = parse_notes_into_jira_tasks(notes)
        if not tasks:
            return "⚠️ No valid tasks found."

        msgs = []
        for task in tasks:
            title = task.get("title")
            description = task.get("description")
            issue_type = task.get("ticket_type", "Task")
            priority = task.get("priority")
            due_date = task.get("due_date")
            assignee = task.get("assignee")
            assignee_id = lookup_account_id(assignee)

            res = create_jira_ticket(
                title=title,
                description=description,
                issue_type=issue_type,
                priority=priority,
                assignee_id=assignee_id,
                due_date=due_date
            )

            if res:
                url = f"https://{os.getenv('JIRA_DOMAIN')}/browse/{res['key']}"
                msgs.append(f"✅ [{res['key']}]({url}) - {title} ({issue_type})")
            else:
                msgs.append(f"❌ Failed to create: {title}")

        return "\\n".join(msgs)

    except Exception as e:
        return f"❌ Failed to process notes: {str(e)}"

# 🧰 Register tools (all must accept one str input)
tools = [
    Tool(
        name="CreateJiraProject",
        func=create_project_tool,
        description="Use this tool to create a new Jira project. Input should be the project name."
    ),
    Tool(
        name="FullNotesToJira",
        func=full_notes_to_jira,
        description="Use this tool to analyze messy notes, extract tasks, and create Jira tickets for them automatically."
    )
]

# 🤖 Initialize LangChain agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 🧪 Run agent from CLI or Flask
def run_agent(notes: str) -> str:
    return agent.run(notes)
