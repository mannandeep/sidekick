# Sidekick

This repository provides a simple AI assistant that interacts with Jira.

## Backend

The backend is organized as a Python package under `backend/`. Key components include:

- `actions/` – each file implements a single Sidekick action
- `utils/` – helper functions for connecting to Jira and other utilities
- `rag/` – scripts to build and query the FAISS index of Jira issues
- `llm/` – utilities for language-model interactions
- `context/` – context persistence
- `sidekick.py` – orchestrates RAG and invokes actions


These scripts create `backend/jira_memory.json` and the `backend/faiss_index/` directory that `python -m backend` requires.

Before running the assistant you must build the Jira memory snapshot and vector store:

```bash
python -m backend.utils.get_info_from_jira
python -m backend.rag.build_jira_vectorstore
```

These scripts create `jira_memory.json` and the `faiss_index/` directory that `python -m backend` requires.

Run the assistant via:

```bash
python -m backend --notes "my product notes"
```

## Frontend

A minimal web interface is provided under `frontend/`.
