# backend/app/api/export.py
from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.services.export_service import export_markdown, export_pdf


router = APIRouter(prefix="/export", tags=["Export"])


@router.post("/{project_id}/pdf")
def export_pdf_api(project_id: int, user=Depends(get_current_user)):
    markdown = "# Project Documentation\n\n```mermaid\ngraph TD; A-->B;```"
    md = export_markdown(project_id, markdown)
    pdf = export_pdf(md)
    return {"pdf_path": pdf}