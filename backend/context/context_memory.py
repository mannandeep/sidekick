import json
from pathlib import Path

CONTEXT_FILE = Path(__file__).parent / "context_memory.json"

# Default structure
default_context = {
    "active_project_key": None,
    "active_user": None,
    "last_checked": None,
    "default_assignee": None,
    "project_aliases": {}  # e.g., "sidekick" → "AAP"
}

# Load context from file or create new
def get_context():
    if CONTEXT_FILE.exists():
        with open(CONTEXT_FILE, "r") as f:
            return json.load(f)
    else:
        return default_context.copy()

# Save updated context to file
def update_context(new_context):
    with open(CONTEXT_FILE, "w") as f:
        json.dump(new_context, f, indent=2)

# Utility to update a specific field
def set_context_field(field, value):
    context = get_context()
    context[field] = value
    update_context(context)

# Shortcut: Get the active project
def get_active_project_key():
    return get_context().get("active_project_key")

