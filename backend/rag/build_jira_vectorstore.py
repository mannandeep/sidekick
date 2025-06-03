import json
from pathlib import Path
from dotenv import load_dotenv
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Load .env variables
load_dotenv()

# 📥 Load Jira memory from file
def load_jira_issues(filename: str | None = None):
    if filename is None:
        filename = Path(__file__).parent.parent / "jira_memory.json"
    else:
        filename = Path(filename)
    with open(filename, "r") as f:
        data = json.load(f)

    docs = []
    for project in data.get("projects", []):
        project_key = project.get("key")
        project_name = project.get("name")
        for issue in project.get("issues", []):
            comments = issue.get("comments", [])
            extracted_comments = []

            for c in comments:
                if "body" in c and "content" in c["body"]:
                    blocks = c["body"]["content"]
                    for block in blocks:
                        for span in block.get("content", []):
                            if "text" in span:
                                extracted_comments.append(span["text"])

            comment_text = " | ".join(extracted_comments)
            summary = issue.get("summary") or "No summary"
            status = issue.get("status") or "Unknown"
            assignee = issue.get("assignee") or "Unassigned"
            updated = issue.get("updated") or "Unknown"

            issue_text = f"""[Project: {project_name} ({project_key})]
Issue Key: {issue.get("key")}
Summary: {summary}
Status: {status}
Assignee: {assignee}
Last Updated: {updated}
Comments: {comment_text if comment_text else "No comments available."}"""

            doc = Document(
                page_content=issue_text,
                metadata={"project": project_key, "issue_key": issue.get("key")}
            )
            docs.append(doc)

    return docs

# 🔤 Load embedding model
def get_embedding_model():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 💾 Create vector index
def create_vectorstore(docs, index_path: str | None = None):
    if index_path is None:
        index_path = Path(__file__).parent.parent / "faiss_index"
    else:
        index_path = Path(index_path)
    embedding = get_embedding_model()
    vectorstore = FAISS.from_documents(docs, embedding)
    vectorstore.save_local(str(index_path))
    print(f"✅ Vectorstore saved to: {index_path}")
    return vectorstore

# ▶️ Main
if __name__ == "__main__":
    print("📥 Loading Jira memory...")
    docs = load_jira_issues()
    print(f"🧾 {len(docs)} issues loaded.")

    print("📦 Creating improved vector store with richer issue context...")
    create_vectorstore(docs)
