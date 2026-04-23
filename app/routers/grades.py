from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db
from app.models import ExamResult, User
from app.schemas import ExamCreate
from app.services import refresh_gamification
from app.security import require_roles, ROLE_ADMIN, ROLE_TEACHER, ROLE_SECRETARY

router = APIRouter(prefix="/grades", tags=["grades"])


@router.post("")
def add_grade(
    payload: ExamCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(ROLE_ADMIN, ROLE_TEACHER, ROLE_SECRETARY)),
):
    row = ExamResult(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)

    snapshot = refresh_gamification(db, payload.student_id)
    return {
        "grade_id": row.id,
        "gamification": {
            "medal": snapshot.medal,
            "streak_count": snapshot.streak_count,
            "trend": snapshot.trend,
        },
    }


@router.get("/top")
def top_students(limit: int = 10, db: Session = Depends(get_db)):
    rows = db.scalars(select(ExamResult).order_by(ExamResult.score.desc()).limit(limit)).all()
    return [
        {
            "student_id": r.student_id,
            "exam_title": r.exam_title,
            "score": r.score,
            "max_score": r.max_score,
        }
        for r in rows
    ]
