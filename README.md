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

## Quick Flow (مهم)
1. اعمل login على `/auth/login` بأي حساب.
2. خُد `token`.
3. في أي endpoint محمي ابعت Header:
   - `X-Token: <token>`

## ملاحظة صريحة
النسخة الحالية Backend كاملة كأساس تشغيلي وقابلة للتجربة الفورية محليًا، لكن **الرفع Production على سيرفر عام** محتاج خطوة نشر (Docker/Cloud/Domain/SSL) خارج بيئة التطوير دي.
