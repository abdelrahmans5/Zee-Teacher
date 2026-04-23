from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db
from app.models import User, Student
from app.schemas import StudentCreate
from app.security import hash_password, require_roles, ROLE_ADMIN, ROLE_SECRETARY, ROLE_TEACHER

router = APIRouter(prefix="/students", tags=["students"])


@router.post("")
def create_student(
    payload: StudentCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles(ROLE_ADMIN, ROLE_SECRETARY, ROLE_TEACHER)),
):
    existing = db.scalar(select(User).where(User.email == payload.email))
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(
        name=payload.name,
        role="student",
        email=payload.email,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    db.flush()

    student = Student(
        user_id=user.id,
        group_name=payload.group_name,
        parent_phone=payload.parent_phone,
        whatsapp_group_link=payload.whatsapp_group_link,
    )
    db.add(student)
    db.commit()
    db.refresh(student)

    return {"student_id": student.id, "user_id": user.id}


@router.get("")
def list_students(group_name: str | None = None, db: Session = Depends(get_db)):
    stmt = select(Student)
    if group_name:
        stmt = stmt.where(Student.group_name == group_name)
    rows = db.scalars(stmt).all()
    return [
        {
            "id": r.id,
            "user_id": r.user_id,
            "group_name": r.group_name,
            "parent_phone": r.parent_phone,
            "whatsapp_group_link": r.whatsapp_group_link,
        }
        for r in rows
    ]
