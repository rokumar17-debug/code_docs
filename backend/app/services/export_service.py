# backend/app/services/export_service.py
from pathlib import Path
import subprocess


EXPORT_DIR = "exports"
Path(EXPORT_DIR).mkdir(exist_ok=True)




def export_markdown(project_id: int, content: str) -> str:
    md_path = f"{EXPORT_DIR}/project_{project_id}.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(content)
    return md_path




def export_pdf(md_path: str) -> str:
    pdf_path = md_path.replace(".md", ".pdf")
    subprocess.run(["pandoc",md_path,"-o",pdf_path,"--pdf-engine=xelatex"])
    return pdf_path