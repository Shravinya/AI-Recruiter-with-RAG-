import os
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

# Load env
load_dotenv()
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_rag")

print(f"✅ Using ChromaDB at: {os.path.abspath(CHROMA_DB_PATH)}")

# Persistent DB client
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

# Embedding function
embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Global collection
jd_collection = client.get_or_create_collection(
    name="job_descriptions",
    embedding_function=embed_fn,
    metadata={"hnsw:space": "cosine"}
)

# -----------------------------
# Insert jobs
# -----------------------------
def insert_jobs(jobs):
    docs, ids, metas = [], [], []
    for i, job in enumerate(jobs):
        jid = f"job-{len(jd_collection.get()['ids']) + i + 1}"
        text = f"Title: {job['title']}\nCompany: {job['company']}\nDescription: {job['description']}"
        docs.append(text)
        ids.append(jid)
        metas.append({"title": job["title"], "company": job["company"]})
    if docs:
        jd_collection.add(documents=docs, metadatas=metas, ids=ids)
    return len(docs)

# -----------------------------
# Get job count
# -----------------------------
def get_job_count():
    return jd_collection.count()
