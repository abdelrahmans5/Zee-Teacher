from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db
from app.models import ExamResult, AIRecommendation, RiskAlert
from app.schemas import RecommendationOut, RiskAlertOut, EssayScoreRequest, EssayScoreResponse
from app.ai.recommendation import build_recommendations
from app.ai.risk import compute_drop_alert
from app.ai.essay import suggest_essay_score
from app.security import get_current_user

router = APIRouter(prefix="/ai", tags=["ai"])


@router.get("/recommendations/{student_id}", response_model=RecommendationOut)
def recommendations(student_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    results = db.scalars(select(ExamResult).where(ExamResult.student_id == student_id)).all()
    recs, acc = build_recommendations(results)

    for rec in recs:
        db.add(AIRecommendation(student_id=student_id, recommendation_text=rec, confidence=acc))
    db.commit()

    return RecommendationOut(student_id=student_id, recommendations=recs, accuracy_estimate=acc)


@router.get("/risk/{student_id}", response_model=RiskAlertOut)
def risk(student_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    results = db.scalars(
        select(ExamResult).where(ExamResult.student_id == student_id).order_by(ExamResult.created_at)
    ).all()
    percentages = [(r.score / r.max_score) * 100 if r.max_score else 0 for r in results]
    drop_percent, high_risk = compute_drop_alert(percentages)

    alert = RiskAlert(student_id=student_id, drop_percent=drop_percent, is_high_risk=high_risk)
    db.add(alert)
    db.commit()

    return RiskAlertOut(student_id=student_id, drop_percent=drop_percent, is_high_risk=high_risk)


@router.post("/essay-score", response_model=EssayScoreResponse)
def essay_score(payload: EssayScoreRequest, _=Depends(get_current_user)):
    score, feedback = suggest_essay_score(payload.answer_text)
    return EssayScoreResponse(score_suggestion=score, feedback=feedback)
