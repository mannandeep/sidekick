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

You can either set Jira credentials in a `.env` file or connect at runtime.

To use environment variables create `.env` with:

```
JIRA_URL=<https://your-domain.atlassian.net>
JIRA_EMAIL=<your@email>
JIRA_API_TOKEN=<token>
JIRA_DOMAIN=<your-domain.atlassian.net>
```

Alternatively call the `/connect_jira` endpoint (or the "Connect to Jira" button
in the web UI) and provide your Jira URL, email and API token. Credentials are
stored in `backend/jira_credentials.json`.

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
Use the **Connect to Jira** button in the UI to supply your credentials if you
haven't created a `.env` file.

## Desktop Electron App

A lightweight desktop UI lives in `desktop/`.
To try it out:

```bash
cd desktop
npm install
npm start
```

The Electron window connects to the backend at `http://localhost:5000` so make
sure the API server is running first:

```bash
python -m backend serve
```

## License

This project is licensed under the [MIT License](LICENSE).
