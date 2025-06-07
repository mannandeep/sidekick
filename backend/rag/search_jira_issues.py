
from pathlib import Path
import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Load the embedding model and vectorstore

def load_vectorstore(index_path: str | None = None):
    if index_path is None:
        index_path = Path(__file__).parent.parent / "faiss_index"
    else:
        index_path = Path(index_path)

    embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local(
        str(index_path), embeddings=embedding, allow_dangerous_deserialization=True
    )
    return vectorstore

# Search for similar Jira issues
def search_similar_issues(query, k=3):
    vectorstore = load_vectorstore()
    results = vectorstore.similarity_search(query, k=k)
    print(f"\n🔍 Top {k} matches for: '{query}'\n")
    for i, doc in enumerate(results, start=1):
        print(f"Result {i}:")
        print(doc.page_content)
        print("-" * 60)

if __name__ == "__main__":
    query = input("📝 Enter your Jira-related query: ")
    search_similar_issues(query)
