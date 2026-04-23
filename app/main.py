from fastapi import FastAPI
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import Base, engine, SessionLocal
from app.models import User, Student
from app.security import hash_password
from app.routers import (
    auth,
    students,
    attendance,
    grades,
    finance,
    ai,
    schedule,
    notifications,
    leaderboard,
    parent,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Zee Teacher System API", version="1.0.0")

app.include_router(auth.router)
app.include_router(students.router)
app.include_router(schedule.router)
app.include_router(attendance.router)
app.include_router(grades.router)
app.include_router(finance.router)
app.include_router(ai.router)
app.include_router(notifications.router)
app.include_router(leaderboard.router)
app.include_router(parent.router)


def seed_demo_data():
    db: Session = SessionLocal()
    try:
        admin = db.scalar(select(User).where(User.email == "admin@zee.local"))
        if not admin:
            users = [
                User(name="System Admin", role="admin", email="admin@zee.local", hashed_password=hash_password("Admin@123")),
                User(name="Teacher One", role="teacher", email="teacher@zee.local", hashed_password=hash_password("Teacher@123")),
                User(name="Secretary One", role="secretary", email="secretary@zee.local", hashed_password=hash_password("Secretary@123")),
                User(name="Parent One", role="parent", email="parent@zee.local", hashed_password=hash_password("Parent@123")),
                User(name="Student One", role="student", email="student@zee.local", hashed_password=hash_password("Student@123")),
            ]
            for u in users:
                db.add(u)
            db.flush()

            student_user = db.scalar(select(User).where(User.email == "student@zee.local"))
            if student_user:
                db.add(
                    Student(
                        user_id=student_user.id,
                        group_name="G1",
                        parent_phone="01000000000",
                        whatsapp_group_link="https://chat.whatsapp.com/demo",
                    )
                )
            db.commit()
    finally:
        db.close()


seed_demo_data()


@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}
