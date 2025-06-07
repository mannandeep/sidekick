# Sidekick

This repository provides a simple AI assistant that interacts with Jira.

## Backend

The backend is organized as a Python package under `backend/`. Key components include:

- `actions/` – each file implements a single Sidekick action
- `utils/` – helper functions for connecting to Jira and other utilities
- `rag/` – scripts to build and query the FAISS index of Jira issues
- `context/` – context persistence
- `sidekick.py` – orchestrates RAG and invokes actions



Before running the assistant you must build the Jira memory snapshot and vector store:

```bash
python -m backend.utils.get_info_from_jira
python -m backend.rag.build_jira_vectorstore
```

These scripts create `backend/jira_memory.json` and the `backend/faiss_index/` directory that `python -m backend` requires.


Run the assistant via CLI or start the HTTP API.

### Environment

Create a `.env` file with:

```
JIRA_URL=<https://your-domain.atlassian.net>
JIRA_EMAIL=<your@email>
JIRA_API_TOKEN=<token>
JIRA_DOMAIN=<your-domain.atlassian.net>
```

### Build Memory and Vector Store

```bash
python -m backend.utils.get_info_from_jira
python -m backend.rag.build_jira_vectorstore
```

### CLI Usage

Process notes directly:

```bash
python -m backend run --notes "my product notes"
```

Set context fields:

```bash
python -m backend set-project AAP
python -m backend set-assignee amit
```

### HTTP API

```bash
python -m backend serve
```

POST `/sidekick` with `{ "notes": "..." }` to get a response.

## Frontend

A minimal web interface is provided under `frontend/`.

## License

This project is licensed under the [MIT License](LICENSE).
