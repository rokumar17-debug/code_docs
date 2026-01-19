# # backend/app/services/semantic_index.py
# from sqlalchemy.orm import Session
# from app.services.embedding_service import embed_text
# from app.models.code_embedding import CodeEmbedding




# def index_code(db: Session, project_id: int, file: str, content: str):
#     emb = embed_text(content)
#     db.add(CodeEmbedding(
#     project_id=project_id,
#     file_path=file,
#     content=content,
#     embedding=emb
#     ))
#     db.commit()

# backend/app/services/semantic_index.py
from sqlalchemy.orm import Session
from app.services.embedding_service import embed_text
from app.models.code_embedding import CodeEmbedding


def index_code(
    db: Session,
    project_id: int,
    file_path: str,
    content: str
):
    """
    Store code embedding into pgvector table
    """
    embedding = embed_text(content)

    row = CodeEmbedding(
        project_id=project_id,
        file_path=file_path,
        content=content,
        embedding=embedding
    )

    db.add(row)
    db.commit()
    db.refresh(row)

    return row.id
