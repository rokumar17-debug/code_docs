# ================================
# backend/app/core/security.py (UPDATED)
# ================================
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session


from app.core.database import get_db
from app.models.user import User


SECRET_KEY = "CHANGE_ME_SUPER_SECRET"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")




def hash_password(password: str) -> str:
    return pwd_context.hash(password[:72])




def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password[:72], hashed)




def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)




# ================================
# JWT DEPENDENCIES
# ================================


def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate": "Bearer"},)


    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception


    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    
    return user




def get_current_admin(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Admin access required")
    return user

