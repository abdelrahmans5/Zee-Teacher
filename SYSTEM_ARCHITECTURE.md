# System Architecture — Zee Teacher Platform

## 1) Product Vision
بناء نظام موحد يدير:
- تشغيل الأكاديمية اليومية (جداول، حضور، درجات، واجبات، تقارير، صلاحيات).
- إدارة مالية وتشغيلية للإيرادات والمصروفات.
- تجربة طلابية تفاعلية ومحفزة (Gamification + Leaderboard).
- تجربة ولي أمر واضحة ومباشرة مع تنبيهات فورية.
- طبقة AI تدريجية (توصيات، إنذار مبكر، مساعدين ذكيين).

---

## 2) Stakeholders & Portals

### 2.1 Teacher Portal
- Calendar (يومي/أسبوعي/شهري) + رسائل موجهة لمجموعات الأوفلاين.
- Attendance Viewer لحظي.
- Grading Dashboard مع فلاتر/Sorting قوي.
- Gamification (medals, streaks, trend arrows).
- تقارير تقييم ونمو أكاديمي.
- Financial Dashboard + Ledger.
- إدارة صلاحيات السكرتارية والتفويض.

### 2.2 Secretary Portal
- Student registry + أرقام أولياء الأمور + روابط WhatsApp.
- تسجيل حضور سريع عبر Keyboard-first UX.
- إدارة مدفوعات + إيصال رقمي.
- إنشاء وإرسال تقارير أولياء الأمور Bulk.
- رفع محتوى ودعم بنك الأسئلة ضمن الصلاحيات.
- تعديل الجداول الرسمية.

### 2.3 Student Portal
- محتوى منظم حسب Unit/Lesson + Progress tracker.
- اختبارات تفاعلية + تصحيح فوري للأسئلة الموضوعية.
- رفع واجبات + استلام Feedback.
- لوحة أداء شخصية + Gamification.
- عرض Leaderboard بدون بيانات حساسة.

### 2.4 Parent Portal
- تنبيهات الغياب الآلية.
- ملخص أكاديمي + ملخص مالي.
- تقارير شهرية سهلة الوصول.
- (اختياري P2) تكامل Telegram Bot.

### 2.5 Admin / System Ops
- إدارة الأدوار والسياسات.
- Audit logs, security controls, backup & recovery.
- Monitoring & alerting.

---

## 3) Domain Modules

1. **Identity & Access (IAM)**
   - RBAC + Delegated permissions.
   - MFA + Step-up auth للعمليات الحساسة (حذف شامل / تعديل صلاحيات عالية).
   - Session management + device tracking.

2. **Academic Operations**
   - Scheduling engine.
   - Attendance engine.
   - Grading & assessment.
   - Assignments & quizzes.

3. **Content Management (CMS/LMS)**
   - Units/Lessons + drag-drop ordering.
   - Media upload + encoding pipeline + secure streaming.
   - Question bank + randomization engine.

4. **Communication & Notifications**
   - In-app notifications.
   - WhatsApp/SMS/Email gateways.
   - Event-driven alerts (absence, new homework, schedule updates).

5. **Gamification Engine**
   - Medals (High Score / Most Improved).
   - Streak calculation (e.g. 90%+ consecutive).
   - Trend indicator مقارنة آخر 3 امتحانات.
   - Leaderboard daily refresh.

6. **Reporting & Analytics**
   - Student-level growth reports.
   - Teacher & management dashboards.
   - Financial monthly analytics.

7. **Finance Module**
   - Fee plans, dues, payments, receipts.
   - Monthly P&L (income, expenses, net).
   - Detailed ledger.

8. **AI Services (Phase 2)**
   - Personalized recommendation model.
   - Predictive decline/dropout risk.
   - Curriculum Q&A chatbot.
   - Essay scoring assist.

---

## 4) Suggested Technical Architecture

- **Frontend**: Next.js (Teacher/Secretary/Student/Parent portals) + responsive UI.
- **Backend**: NestJS/FastAPI modular monolith (قابل للتحول لـ microservices لاحقًا).
- **Database**: PostgreSQL (OLTP) + Redis (cache, queues metadata).
- **Object Storage**: S3-compatible for videos/files.
- **Message Broker**: RabbitMQ/Kafka (events for notifications, gamification, analytics).
- **Search**: OpenSearch/Elasticsearch (global search < 3 sec at 10k+ records).
- **Media Pipeline**: FFmpeg workers for encoding/compression/HLS.
- **Observability**: Prometheus + Grafana + centralized logs (ELK/OpenSearch).
- **Security Layer**: WAF + rate limiting + audit trails + secrets manager.

### Monolith-first, Event-driven-inside
- نبدأ بـ Modular Monolith لتقليل التعقيد وسرعة التسليم.
- نفصل وحدات ثقيلة بالـ events داخليًا (notifications, gamification, reporting).
- عند الحمل العالي يتم فصل modules تدريجيًا لخدمات مستقلة.

---

## 5) Data Model (Core Entities)

- `users` (teacher, secretary, student, parent, admin)
- `roles`, `permissions`, `role_permissions`, `user_permissions`
- `students`, `parents`, `student_parent_links`
- `groups`, `classes`, `enrollments`, `schedules`, `sessions`
- `attendance_records`
- `exams`, `questions`, `question_bank_tags`, `exam_attempts`, `grades`
- `assignments`, `submissions`, `feedback`
- `units`, `lessons`, `materials`, `media_assets`, `lesson_progress`
- `payment_transactions`, `expenses`, `ledger_entries`, `receipts`
- `notifications`, `notification_deliveries`, `message_templates`
- `gamification_snapshots` (medals, streak, trend)
- `leaderboard_snapshots`
- `audit_logs`
- `ai_features`, `ai_predictions`, `ai_recommendations`

---

## 6) Key Workflows (Mapped to Acceptance Criteria)

### 6.1 Offline Session Messaging (Teacher)
1. Teacher opens calendar.
2. Select offline session.
3. Click “Message Session Students”.
4. Template + send.
5. Delivery status visible.

**SLA**: <10s لإتمام العملية.

### 6.2 Secretary Attendance (30 students / 60 sec)
1. Keyboard mode + quick mark (P/A/L).
2. Bulk patterns (all present then exceptions).
3. Submit once.
4. Teacher sees live update in <=3 sec at class start.

### 6.3 Grade Update -> Gamification Refresh
1. New exam grade saved.
2. Event emitted.
3. Gamification engine recalculates medal/streak/trend.
4. Student dashboard updates instantly; leaderboard refresh (hourly/daily).

### 6.4 Payment Logging + Receipt
1. Search student.
2. Enter amount/method/reference.
3. Auto-generate digital receipt (PDF + unique ID).
4. Optional send to parent via WhatsApp/SMS/email.

---

## 7) API Surface (High-Level)

- `POST /auth/login`, `POST /auth/mfa/verify`
- `GET /teacher/calendar`, `POST /teacher/sessions/{id}/message`
- `GET /attendance/group/{id}`, `POST /attendance/bulk`
- `GET /grades`, `POST /grades`, `GET /grades/top?limit=10`
- `GET /gamification/student/{id}`
- `GET /reports/student/{id}/growth`
- `POST /finance/payments`, `GET /finance/dashboard/monthly`
- `POST /admin/secretaries/{id}/permissions`
- `POST /content/media/upload`, `POST /content/units/reorder`
- `GET /search?q=...`
- `POST /notifications/publish`
- `GET /parent/student/{id}/summary`
- `POST /integrations/telegram/webhook`

---

## 8) Security & Compliance

- MFA mandatory for teachers/admins.
- Re-auth password challenge for destructive actions.
- RBAC + per-action permission checks.
- Immutable audit logs لكل تعديل/حذف.
- Encryption in transit (TLS) and at rest.
- PII minimization + data masking.
- AI training only on anonymized data.
- WAF policies against SQLi/XSS + regular pentest before launch.

---

## 9) Performance Targets (NFR)

- Attendance visibility update: <= 3 sec.
- Top-10 ranking query: <= 2 sec.
- Large report (500+ students): <= 5 sec.
- Global search (10k+ records): <= 3 sec.
- Parent data freshness: <= 15 min.
- Home page at 500 concurrent users: <= 4 sec.
- Notifications dispatch latency: <= 10 sec (homework) and <= 5 min (absence to parent).

---

## 10) Implementation Roadmap

### Phase 1 (Must Have / P1) — 12 to 16 weeks
- IAM + MFA + Audit Log.
- Scheduling + attendance + messaging.
- Grades dashboard + gamification basics.
- Student/parent portals الأساسية.
- Finance core + receipts + monthly dashboard.
- CMS core + question bank + search.
- Infra baseline (CI/CD, monitoring, backups).

### Phase 2 (Should Have / P2) — 8 to 12 weeks
- Advanced reports + growth analytics.
- Leaderboard public enhancements.
- Telegram bot integration.
- AI recommendation + predictive alerts.
- Essay scoring assistant.

### Phase 3 (Optimization)
- Scalability hardening.
- A/B testing for UX flows.
- Model quality tuning + MLOps pipeline.

---

## 11) Delivery Plan by Team

- **Backend Team**: IAM, academic, finance, notifications, reports APIs.
- **Frontend Team**: portals + keyboard-first attendance + responsive UX.
- **Data/AI Team**: feature store, model training/inference, monitoring drift.
- **DevOps/SecOps**: WAF, CI/CD, observability, backups, secrets, pentest.
- **QA Team**: SLA tests + regression + security + UAT with teachers/secretaries.

---

## 12) UAT Scenarios (Examples)

1. Teacher removes secretary permission “Add Student” in <30 sec.
2. Secretary adds student + parent number + WhatsApp link in <60 sec.
3. Secretary logs 30 attendances in <=60 sec (keyboard-only).
4. Teacher retrieves Top-10 in <=2 sec with filters.
5. Parent receives absence alert in <=5 min.
6. Student sees quiz objective score <=2 sec after submit.
7. 500MB video upload + processing + secure play <=5 min.

---

## 13) Risks & Mitigations

- **Notification provider dependency** → multi-provider fallback.
- **Heavy media processing** → async workers + autoscaling.
- **Data consistency under concurrency** → transactional boundaries + idempotent events.
- **AI false positives** → human-in-the-loop + threshold tuning.
- **Permission complexity** → policy simulator + audit explainability.

---

## 14) Definition of Done (Per Feature)

- Functional acceptance criteria met with measurable SLA.
- Security checks passed (authz, logs, destructive confirmation).
- Performance benchmark passed.
- Monitoring dashboards and alerts configured.
- Documentation + runbook updated.

