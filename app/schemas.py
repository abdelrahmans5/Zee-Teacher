from datetime import datetime
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    token: str
    role: str
    user_id: int


class StudentCreate(BaseModel):
    name: str
    email: str
    password: str
    group_name: str
    parent_phone: str
    whatsapp_group_link: str = ""


class ScheduleCreate(BaseModel):
    title: str
    group_name: str
    teacher_user_id: int
    starts_at: datetime
    ends_at: datetime
    is_offline: bool = True


class AttendanceMark(BaseModel):
    student_id: int
    status: str = Field(pattern="^(present|absent|late)$")


class AttendanceBulkRequest(BaseModel):
    session_id: int
    records: list[AttendanceMark]


class ExamCreate(BaseModel):
    student_id: int
    exam_title: str
    unit_name: str = "General"
    score: float
    max_score: float = 100


class PaymentCreate(BaseModel):
    student_id: int
    amount: float
    method: str
    reference: str


class AssignmentCreate(BaseModel):
    title: str
    group_name: str
    due_at: datetime


class RecommendationOut(BaseModel):
    student_id: int
    recommendations: list[str]
    accuracy_estimate: float


class RiskAlertOut(BaseModel):
    student_id: int
    drop_percent: float
    is_high_risk: bool


class EssayScoreRequest(BaseModel):
    answer_text: str


class EssayScoreResponse(BaseModel):
    score_suggestion: float
    feedback: str
