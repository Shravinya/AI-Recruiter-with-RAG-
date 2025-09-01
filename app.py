import streamlit as st
from parsers import parse_jobs_from_text
from analyzer import analyze_resume
from db import get_job_count, insert_jobs, jd_collection

# -----------------------------
# Streamlit Config
# -----------------------------
st.set_page_config(page_title="🤖 AI Recruiter RAG", page_icon="📄", layout="wide")

st.title("🤖 AI Recruiter with RAG (LangChain + Gemini + ChromaDB)")

# -----------------------------
# Sidebar: Job Database
# -----------------------------
st.sidebar.header("📥 Job Database")

# Always show current count
current_count = get_job_count()
st.sidebar.markdown(f"📊 **Current DB entries:** {current_count}")

job_text = st.sidebar.text_area("Paste job descriptions (--- separated)", height=200)

if st.sidebar.button("➕ Insert into DB"):
    if not job_text.strip():
        st.sidebar.warning("⚠️ Please paste job descriptions first.")
    else:
        jobs = parse_jobs_from_text(job_text)
        count = insert_jobs(jobs)
        new_count = get_job_count()
        st.sidebar.success(f"✅ Inserted {count} job(s). Total now: {new_count}")

# Delete button
if st.sidebar.button("🗑️ Clear DB"):
    jd_collection.delete(where={})
    st.sidebar.error("⚠️ All job descriptions deleted.")
    st.sidebar.markdown("**📊 Current DB entries: 0**")

# Preview recent jobs (Title + Company)
if current_count > 0:
    jobs_preview = jd_collection.get(limit=5)
    st.sidebar.markdown("### 🔎 Last Inserted Jobs")
    for meta in jobs_preview["metadatas"]:
        st.sidebar.write(f"- **{meta['title']}** @ {meta['company']}")

# -----------------------------
# Resume Analysis
# -----------------------------
st.header("📄 Resume Analysis")

resume_text = st.text_area("Paste candidate resume here", height=250)

if st.button("🔍 Analyze Resume"):
    if not resume_text.strip():
        st.warning("⚠️ Please paste a resume first.")
    else:
        with st.spinner("Analyzing resume with Gemini..."):
            result = analyze_resume(resume_text)

        st.subheader("✅ Recruiter Summary")
        st.markdown(f"<div style='padding:1em; border-radius:10px; background:#e6ffed; color:#1b4332;'>{result}</div>", unsafe_allow_html=True)
