from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db
from app.models import ScheduleSession
from app.schemas import ScheduleCreate
from app.security import require_roles, ROLE_ADMIN, ROLE_TEACHER, ROLE_SECRETARY

router = APIRouter(prefix="/schedule", tags=["schedule"])


@router.post("")
def create_schedule(
    payload: ScheduleCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles(ROLE_ADMIN, ROLE_SECRETARY, ROLE_TEACHER)),
):
    session = ScheduleSession(**payload.model_dump())
    db.add(session)
    db.commit()
    db.refresh(session)
    return {"session_id": session.id}


@router.get("")
def list_schedule(group_name: str | None = None, db: Session = Depends(get_db)):
    stmt = select(ScheduleSession)
    if group_name:
        stmt = stmt.where(ScheduleSession.group_name == group_name)

    rows = db.scalars(stmt.order_by(ScheduleSession.starts_at)).all()
    return [
        {
            "id": r.id,
            "title": r.title,
            "group_name": r.group_name,
            "teacher_user_id": r.teacher_user_id,
            "starts_at": r.starts_at,
            "ends_at": r.ends_at,
            "is_offline": r.is_offline,
        }
        for r in rows
    ]
