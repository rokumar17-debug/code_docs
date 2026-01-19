# # backend/app/api/search.py
# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from app.core.database import get_db
# from app.services.embedding_service import embed_text


# router = APIRouter(prefix="/search", tags=["Search"])


# @router.get("/")
# def search(project_id: int, q: str, db: Session = Depends(get_db)):
#     emb = embed_text(q)
#     result = db.execute("""
#     SELECT file_path, content
#     FROM code_embeddings
#     ORDER BY embedding <-> :emb
#     LIMIT 5
#     """, {"emb": emb})


#     return [{"file": r[0], "snippet": r[1][:200]} for r in result]


# # backend/app/api/search.py
# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from sqlalchemy import text

# from app.core.database import get_db
# from app.core.security import get_current_user
# from app.services.embedding_service import embed_text

# router = APIRouter(prefix="/search", tags=["Search"])


# @router.get("/")
# def search_code(
#     project_id: int,
#     q: str,
#     db: Session = Depends(get_db),
#     user=Depends(get_current_user)
# ):
#     query_embedding = embed_text(q)

#     sql = text("""
#         SELECT file_path, content
#         FROM code_embeddings
#         WHERE project_id = :project_id
#         ORDER BY embedding <-> :embedding
#         LIMIT 5
#     """)

#     result = db.execute(
#         sql,
#         {
#             "project_id": project_id,
#             "embedding": query_embedding
#         }
#     ).fetchall()

#     return [
#         {
#             "file": row.file_path,
#             "snippet": row.content[:200]
#         }
#         for row in result
#     ]

# backend/app/api/search.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.database import get_db
from app.services.embedding_service import embed_text
from app.core.security import get_current_user

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/")
def search_code(
    project_id: int,
    q: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    embedding = embed_text(q)

    sql = text("""
        SELECT file_path, content
        FROM code_embeddings
        WHERE project_id = :project_id
        ORDER BY embedding <-> (:embedding)::vector
        LIMIT 5
    """)

    results = db.execute(
        sql,
        {
            "project_id": project_id,
            "embedding": embedding
        }
    ).fetchall()

    return [
        {
            "file": r[0],
            "snippet": r[1][:300]
        }
        for r in results
    ]

