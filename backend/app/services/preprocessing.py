# ---------------------------------------------------------
# backend/app/services/preprocessing.py (MILESTONE 2)
# ---------------------------------------------------------
import os


IGNORE_DIRS = {".git", "node_modules", "__pycache__"}
CODE_EXTENSIONS = {".py", ".js", ".ts"}




def preprocess_repository(repo_path: str):
    files = []
    for root, dirs, filenames in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for file in filenames:
            ext = os.path.splitext(file)[1]
            if ext in CODE_EXTENSIONS:
                files.append(os.path.join(root, file))
    return {
    "repo_type": "FastAPI" if any("fastapi" in f.lower() for f in files) else "Unknown",
    "file_count": len(files),
    "files": files
    }