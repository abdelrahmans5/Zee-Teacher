from datetime import datetime, timedelta
from uuid import uuid4

from fastapi import Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, SessionToken
from app.crypto import hash_password, verify_password


ROLE_ADMIN = "admin"
ROLE_TEACHER = "teacher"
ROLE_SECRETARY = "secretary"
ROLE_STUDENT = "student"
ROLE_PARENT = "parent"



def create_session_token(db: Session, user_id: int, ttl_hours: int = 12) -> str:
    token = uuid4().hex
    session = SessionToken(user_id=user_id, token=token, expires_at=datetime.utcnow() + timedelta(hours=ttl_hours))
    db.add(session)
    db.commit()
    return token


def get_current_user(x_token: str = Header(default=""), db: Session = Depends(get_db)) -> User:
    if not x_token:
        raise HTTPException(status_code=401, detail="Missing X-Token header")

    session = db.scalar(select(SessionToken).where(SessionToken.token == x_token))
    if not session or session.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.scalar(select(User).where(User.id == session.user_id))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def require_roles(*roles: str):
    def checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user

    return checker
