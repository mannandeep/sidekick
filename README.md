# Sidekick

This repository provides a simple AI assistant that interacts with Jira.

## Backend

The backend is organized as a Python package under `backend/`. Key components include:

- `actions/` – each file implements a single Sidekick action
- `jira/` – helpers for interacting with Jira
- `rag/` – scripts to build and query the FAISS index of Jira issues
- `llm/` – utilities for language-model interactions
- `context/` – context persistence
- `sidekick.py` – orchestrates RAG and invokes actions

Run the assistant via:

```bash
python -m backend --notes "my product notes"
```

## Frontend

A minimal web interface is provided under `frontend/`.
