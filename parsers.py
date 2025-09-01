import uuid

def parse_jobs_from_text(raw_text: str):
    """Parse job descriptions into structured JSON."""
    blocks = [b.strip() for b in raw_text.split("\n---") if b.strip()]
    jobs = []
    for b in blocks:
        title = company = desc = ""
        for line in b.splitlines():
            if line.lower().startswith("title:"):
                title = line.split(":", 1)[1].strip()
            elif line.lower().startswith("company:"):
                company = line.split(":", 1)[1].strip()
            elif line.lower().startswith("description:"):
                desc = line.split(":", 1)[1].strip()
            else:
                if desc:
                    desc += " " + line.strip()
        if title or company or desc:
            jobs.append({
                "id": str(uuid.uuid4()),
                "title": title or "(Untitled Role)",
                "company": company or "",
                "description": desc or "",
            })
    return jobs
