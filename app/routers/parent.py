from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.database import get_db
from app.models import Student, ExamResult, AttendanceRecord, PaymentTransaction
from app.security import get_current_user, ROLE_PARENT

router = APIRouter(prefix="/parent", tags=["parent"])


@router.get('/student-summary/{student_id}')
def parent_summary(student_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user.role != ROLE_PARENT:
        raise HTTPException(status_code=403, detail='Only parent can access this endpoint')

    student = db.scalar(select(Student).where(Student.id == student_id))
    if not student:
        raise HTTPException(status_code=404, detail='Student not found')

    last3 = db.scalars(
        select(ExamResult).where(ExamResult.student_id == student_id).order_by(ExamResult.created_at.desc()).limit(3)
    ).all()
    attendance_total = db.scalar(
        select(func.count(AttendanceRecord.id)).where(AttendanceRecord.student_id == student_id)
    ) or 0
    absent_total = db.scalar(
        select(func.count(AttendanceRecord.id)).where(
            AttendanceRecord.student_id == student_id,
            AttendanceRecord.status == 'absent'
        )
    ) or 0
    paid = db.scalar(select(func.coalesce(func.sum(PaymentTransaction.amount), 0)).where(
        PaymentTransaction.student_id == student_id
    )) or 0

    return {
        'student_id': student_id,
        'last_3_scores': [r.score for r in last3],
        'attendance_total': attendance_total,
        'absent_total': absent_total,
        'paid_amount': float(paid),
    }
