from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ExamResult, GamificationSnapshot


def refresh_gamification(db: Session, student_id: int) -> GamificationSnapshot:
    results = db.scalars(
        select(ExamResult).where(ExamResult.student_id == student_id).order_by(ExamResult.created_at.desc())
    ).all()

    percentages = [(r.score / r.max_score) * 100 if r.max_score else 0 for r in results]
    latest = percentages[0] if percentages else 0

    streak = 0
    for p in percentages:
        if p >= 90:
            streak += 1
        else:
            break

    if len(percentages) >= 4:
        prev3 = sum(percentages[1:4]) / 3
        trend = "up" if latest > prev3 else "down" if latest < prev3 else "steady"
    else:
        trend = "steady"

    medal = ""
    if latest >= 95:
        medal = "High Score"
    elif len(percentages) >= 2 and (latest - percentages[1]) >= 20:
        medal = "Most Improved"

    snap = db.scalar(select(GamificationSnapshot).where(GamificationSnapshot.student_id == student_id))
    if not snap:
        snap = GamificationSnapshot(student_id=student_id)
        db.add(snap)

    snap.medal = medal
    snap.streak_count = streak
    snap.trend = trend
    snap.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(snap)
    return snap
