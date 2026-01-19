


# ================================
# backend/app/api/auth.py (UPDATED)
# ================================
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.schemas.auth import SignupRequest, LoginRequest


router = APIRouter()




@router.post("/signup")
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")


    user = User(
    email=payload.email,
    password=hash_password(payload.password),
    is_admin=payload.is_admin
    )
    db.add(user)
    db.commit()
    return {"message": "Signup successful"}




@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")


    token = create_access_token({
    "sub": user.email,
    "is_admin": user.is_admin
    })


    return {
    "access_token": token,
    "token_type": "bearer"
    }

