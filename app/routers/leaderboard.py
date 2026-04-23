from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ExamResult

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.get("/top")
def leaderboard_top(limit: int = 5, db: Session = Depends(get_db)):
    rows = db.scalars(select(ExamResult).order_by(ExamResult.score.desc()).limit(limit)).all()
    return [{"student_id": r.student_id, "score": r.score, "exam_title": r.exam_title} for r in rows]
