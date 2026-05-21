from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.database import get_db
from app.models import User, AuditLog
from app.config import settings
from pydantic import BaseModel, EmailStr
from typing import Optional

router = APIRouter()
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RegisterIn(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

def hash_pw(p): return pwd.hash(p)
def verify_pw(plain, hashed): return pwd.verify(plain, hashed)

def make_token(user_id: int, email: str) -> str:
    exp = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    return jwt.encode({"sub": str(user_id), "email": email, "exp": exp}, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

async def auth_required(authorization: str = Header(None), db: Session = Depends(get_db)) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(authorization.replace("Bearer ", ""), settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user = db.query(User).filter(User.id == int(payload["sub"])).first()
        if not user: raise HTTPException(status_code=401, detail="User not found")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def user_out(u: User):
    return {"id": u.id, "name": u.name, "email": u.email, "role": u.role, "disclaimer_accepted": u.disclaimer_accepted, "preferred_language": u.preferred_language, "created_at": u.created_at.isoformat()}

@router.post("/register")
def register(data: RegisterIn, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(400, "Email already registered")
    u = User(name=data.name, email=data.email, password_hash=hash_pw(data.password))
    db.add(u)
    db.commit()
    db.refresh(u)
    return {"access_token": make_token(u.id, u.email), "token_type": "bearer", "user": user_out(u)}

@router.post("/login")
def login(data: LoginIn, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.email == data.email).first()
    if not u or not verify_pw(data.password, u.password_hash):
        raise HTTPException(401, "Invalid credentials")
    db.add(AuditLog(user_id=u.id, action="login", resource_type="auth", log_data={}))
    db.commit()
    return {"access_token": make_token(u.id, u.email), "token_type": "bearer", "user": user_out(u)}

@router.post("/demo-login")
def demo_login(db: Session = Depends(get_db)):
    u = db.query(User).filter(User.is_demo == True).first()
    if not u: raise HTTPException(404, "Demo user not found. Run seed.")
    return {"access_token": make_token(u.id, u.email), "token_type": "bearer", "user": user_out(u)}

@router.get("/me")
def me(current_user: User = Depends(auth_required)):
    return user_out(current_user)

@router.post("/accept-disclaimer")
def accept_disclaimer(current_user: User = Depends(auth_required), db: Session = Depends(get_db)):
    current_user.disclaimer_accepted = True
    db.commit()
    return {"message": "Disclaimer accepted"}
