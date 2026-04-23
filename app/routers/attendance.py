from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db
from app.models import AttendanceRecord, User
from app.schemas import AttendanceBulkRequest
from app.security import get_current_user, require_roles, ROLE_ADMIN, ROLE_SECRETARY

router = APIRouter(prefix="/attendance", tags=["attendance"])


@router.post("/bulk")
def bulk_attendance(
    payload: AttendanceBulkRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(ROLE_ADMIN, ROLE_SECRETARY)),
):
    created = 0
    for item in payload.records:
        rec = AttendanceRecord(
            student_id=item.student_id,
            session_id=payload.session_id,
            status=item.status,
            recorded_by=user.id,
        )
        db.add(rec)
        created += 1

    db.commit()
    return {"created": created, "session_id": payload.session_id}


@router.get("/session/{session_id}")
def list_attendance(session_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    rows = db.scalars(select(AttendanceRecord).where(AttendanceRecord.session_id == session_id)).all()
    return [{"student_id": r.student_id, "status": r.status, "created_at": r.created_at} for r in rows]
