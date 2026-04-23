# Zee Teacher — Full Project (Backend + Frontend)

دلوقتي المشروع فيه:
- **Backend**: FastAPI + SQLAlchemy + Role-based auth + AI modules.
- **Frontend**: React + Vite dashboard starter لتجربة الـ login والـ health والـ leaderboard.

## 1) تشغيل محلي سريع

### Backend
# Zee Teacher — Running System (Backend)

ده إصدار عملي شغال من السيستم، وفيه تسجيل دخول بالأدوار المختلفة + APIs تغطي العمليات الأساسية المطلوبة.

## Features جاهزة الآن
- تسجيل دخول Session Token (`/auth/login`) مع أدوار: Admin / Teacher / Secretary / Student / Parent.
- إدارة الطلاب (إضافة + عرض).
- إدارة الجداول والحصص.
- تسجيل حضور Bulk (للsecretary/admin) + عرض الحضور.
- إدخال درجات + تحديث Gamification تلقائيًا (Medal / Streak / Trend).
- إدارة المدفوعات + Dashboard مالي شهري.
- إشعارات داخلية للمجموعات + صندوق إشعارات لكل مستخدم.
- Leaderboard.
- Parent summary (حضور + آخر درجات + مدفوعات).
- AI Baselines: recommendations + risk alert + essay scoring.

## تشغيل المشروع
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```
Backend docs: `http://127.0.0.1:8000/docs`

### Frontend
```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```
Frontend: `http://127.0.0.1:5173`

## 2) حسابات جاهزة
uvicorn app.main:app --reload
```

Open Swagger:
- http://127.0.0.1:8000/docs

## Accounts جاهزة بعد التشغيل
- Admin: `admin@zee.local` / `Admin@123`
- Teacher: `teacher@zee.local` / `Teacher@123`
- Secretary: `secretary@zee.local` / `Secretary@123`
- Parent: `parent@zee.local` / `Parent@123`
- Student: `student@zee.local` / `Student@123`

## 3) ربط الباك مع Supabase (Postgres)

1. اعمل مشروع جديد على Supabase.
2. من **Project Settings -> Database** انسخ اتصال PostgreSQL URI.
3. في ملف `.env` للباك:
```env
DATABASE_URL=postgresql+psycopg2://USER:PASSWORD@HOST:5432/postgres
CORS_ORIGINS=https://your-frontend-domain.vercel.app,http://localhost:5173
```
4. ثبت Driver:
```bash
pip install psycopg2-binary
```
5. شغل الباك:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

> ملاحظة: الجداول تتكون تلقائيًا من `Base.metadata.create_all` في البداية.

## 4) نشر Frontend + Backend

### Backend (Render / Railway / Fly.io)
- اربط GitHub repo.
- Build command:
```bash
pip install -r requirements.txt
```
- Start command:
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```
- Environment variables:
  - `DATABASE_URL`
  - `CORS_ORIGINS`

### Frontend (Vercel)
- Root directory: `frontend`
- Build command: `npm run build`
- Output directory: `dist`
- Env var:
  - `VITE_API_BASE_URL=https://your-backend-domain`

## 5) رفع الشغل على GitHub (بالخطوات)

```bash
git init
git add .
git commit -m "Initial fullstack setup"
git branch -M main
git remote add origin https://github.com/<username>/<repo>.git
git push -u origin main
```

## 6) Important API flow
1. Login من `/auth/login`.
2. خُد `token`.
3. ابعته في أي request محمي Header:
   - `X-Token: <token>`

## 7) الموجود حاليًا وظيفيًا
- Auth + roles.
- Students + schedule + attendance.
- Grades + gamification.
- Finance + monthly dashboard.
- Notifications + leaderboard.
- Parent summary.
- AI baselines (recommendation / risk / essay).
## Quick Flow (مهم)
1. اعمل login على `/auth/login` بأي حساب.
2. خُد `token`.
3. في أي endpoint محمي ابعت Header:
   - `X-Token: <token>`

## ملاحظة صريحة
النسخة الحالية Backend كاملة كأساس تشغيلي وقابلة للتجربة الفورية محليًا، لكن **الرفع Production على سيرفر عام** محتاج خطوة نشر (Docker/Cloud/Domain/SSL) خارج بيئة التطوير دي.
