

# ================================
# backend/app/schemas/auth.py
# ================================
from pydantic import BaseModel, EmailStr




class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    is_admin: bool = False




class LoginRequest(BaseModel):
    email: EmailStr
    password: str