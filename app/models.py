from datetime import datetime
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    role: Mapped[str] = mapped_column(String(30), index=True)  # admin/teacher/secretary/student/parent
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class SessionToken(Base):
    __tablename__ = "session_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    token: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    group_name: Mapped[str] = mapped_column(String(80), index=True)
    parent_phone: Mapped[str] = mapped_column(String(30))
    whatsapp_group_link: Mapped[str] = mapped_column(String(300), default="")


class ScheduleSession(Base):
    __tablename__ = "schedule_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(140))
    group_name: Mapped[str] = mapped_column(String(80), index=True)
    teacher_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    starts_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    ends_at: Mapped[datetime] = mapped_column(DateTime)
    is_offline: Mapped[bool] = mapped_column(Boolean, default=True)


class AttendanceRecord(Base):
    __tablename__ = "attendance_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), index=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("schedule_sessions.id"), index=True)
    status: Mapped[str] = mapped_column(String(20))  # present/absent/late
    recorded_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ExamResult(Base):
    __tablename__ = "exam_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), index=True)
    exam_title: Mapped[str] = mapped_column(String(120))
    unit_name: Mapped[str] = mapped_column(String(120), default="General")
    score: Mapped[float] = mapped_column(Float)
    max_score: Mapped[float] = mapped_column(Float, default=100)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)


class Assignment(Base):
    __tablename__ = "assignments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(160))
    group_name: Mapped[str] = mapped_column(String(80), index=True)
    due_at: Mapped[datetime] = mapped_column(DateTime)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class PaymentTransaction(Base):
    __tablename__ = "payment_transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), index=True)
    amount: Mapped[float] = mapped_column(Float)
    method: Mapped[str] = mapped_column(String(40))
    reference: Mapped[str] = mapped_column(String(120))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class GamificationSnapshot(Base):
    __tablename__ = "gamification_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), index=True, unique=True)
    medal: Mapped[str] = mapped_column(String(60), default="")
    streak_count: Mapped[int] = mapped_column(Integer, default=0)
    trend: Mapped[str] = mapped_column(String(10), default="steady")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class AIRecommendation(Base):
    __tablename__ = "ai_recommendations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), index=True)
    recommendation_text: Mapped[str] = mapped_column(String(300))
    confidence: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class RiskAlert(Base):
    __tablename__ = "risk_alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), index=True)
    drop_percent: Mapped[float] = mapped_column(Float)
    is_high_risk: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    title: Mapped[str] = mapped_column(String(150))
    body: Mapped[str] = mapped_column(Text)
    channel: Mapped[str] = mapped_column(String(30), default="in_app")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
