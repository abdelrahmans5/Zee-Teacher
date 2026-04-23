from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db
from app.models import Notification, Student, User
from app.security import get_current_user, require_roles, ROLE_ADMIN, ROLE_TEACHER

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post("/group-message")
def send_group_message(
    group_name: str,
    title: str,
    body: str,
    db: Session = Depends(get_db),
    _=Depends(require_roles(ROLE_ADMIN, ROLE_TEACHER)),
):
    students = db.scalars(select(Student).where(Student.group_name == group_name)).all()
    created = 0
    for st in students:
        user = db.scalar(select(User).where(User.id == st.user_id))
        if not user:
            continue
        db.add(Notification(user_id=user.id, title=title, body=body, channel="in_app"))
        created += 1
    db.commit()
    return {"delivered": created, "group_name": group_name}


@router.get("/mine")
def my_notifications(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    rows = db.scalars(
        select(Notification).where(Notification.user_id == user.id).order_by(Notification.created_at.desc())
    ).all()
    return [{"title": r.title, "body": r.body, "created_at": r.created_at} for r in rows]
