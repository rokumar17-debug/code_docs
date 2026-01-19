



# ================================
# backend/app/main.py (UPDATED)
# ================================
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, projects, progress
from app.core.database import Base, engine
from app.api import docs
from app.api import admin
from app.api import analysis
from app.api import search
app = FastAPI(title="Code Analysis API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.on_event("startup")
# def startup():
#     Base.metadata.create_all(bind=engine)

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok"}

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(projects.router)
app.include_router(progress.router)
app.include_router(docs.router)
app.include_router(admin.router)
app.include_router(analysis.router)
app.include_router(search.router)