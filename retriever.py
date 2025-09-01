from db import jd_collection

def retrieve_relevant_jobs(query_text: str, top_k: int = 3):
    """Retrieve jobs most relevant to the query (resume)."""
    if jd_collection.count() == 0:
        return []
    res = jd_collection.query(query_texts=[query_text], n_results=top_k)
    hits = []
    if res and res.get("documents"):
        docs = res["documents"][0]
        metas = res.get("metadatas", [[]])[0]
        for d, m in zip(docs, metas):
            hits.append({"document": d, "meta": m})
    return hits
