# AI-Recruiter-with-RAG-



# 🤖 AI Recruiter with RAG (LangChain + Gemini + ChromaDB + Streamlit)

A lightweight, production-ready app that:

- Stores **job descriptions** in a **persistent ChromaDB** vector store  
- Lets you **paste or upload resumes** (PDF/DOCX/TXT)  
- Uses **LangChain** + **Google Gemini** to generate:  
  - ✅ Fit score  
  - ✅ 5-line recruiter summary  
  - ✅ Best role match  
  - ✅ Select / Not Select decision  

---

## 🔗 Quick Start (TL;DR)

```bash
# 1) Clone & enter
git clone https://github.com/<shravinya>/llm_rag_app.git
cd llm_rag_app

# 2) Create venv
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3) Install deps (pinned to avoid NumPy/Chroma issues)
pip install -r requirements.txt

# 4) Set environment variables
copy .env.example .env   # (Windows)
# or:
cp .env.example .env     # (macOS/Linux)

# 5) Add your Gemini API key to .env

# 6) Run
streamlit run app.py

