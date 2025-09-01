import os
from dotenv import load_dotenv
from retriever import retrieve_relevant_jobs
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Load env
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# ✅ Initialize Gemini with API key
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=API_KEY
)

# 📌 Updated prompt for recruiter summary + best role
prompt_template = """
You are an AI recruiter. Analyze the resume with respect to the job context.

Job Context:
{job_context}

Resume:
{resume}

Return the output in the EXACT format below:

Fit Score: [0-100]

Summary (5 lines max highlighting top skills & keywords):
- Line 1
- Line 2
- Line 3
- Line 4
- Line 5

Best Role Match: [Suggest the single most relevant job title from Job Context]

Decision: [Select / Not Select]
"""

prompt = PromptTemplate(
    input_variables=["job_context", "resume"],
    template=prompt_template
)

def analyze_resume(resume_text: str, top_k: int = 3):
    """Analyze resume against job descriptions and return recruiter summary with best role match."""
    retrieved = retrieve_relevant_jobs(resume_text, top_k=top_k)

    # Build job context bullets
    job_bullets = []
    for i, hit in enumerate(retrieved, 1):
        title = hit["meta"].get("title", "")
        company = hit["meta"].get("company", "")
        desc = ""
        for line in hit["document"].splitlines():
            if line.lower().startswith("description:"):
                desc = line.split(":", 1)[1].strip()
                break
        job_bullets.append(f"{i}. {title} @ {company} — {desc}")

    job_context = "\n".join(job_bullets) if job_bullets else "No related jobs found."
    chain_input = {"job_context": job_context, "resume": resume_text}

    # ✅ Updated: use invoke instead of predict
    response = llm.invoke(prompt.format(**chain_input))
    return response.content if hasattr(response, "content") else str(response)
