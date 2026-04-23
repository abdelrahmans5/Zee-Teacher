# Requirements Traceability Matrix (RTM)

> المصفوفة التالية تربط المتطلبات بالميزات، مخرجات التنفيذ، واختبارات القبول القابلة للقياس.

## Teacher & Management

| ID | Requirement | Priority | Feature/Module | KPI / Acceptance Test |
|---|---|---|---|---|
| T1 | Scheduling & Communication | P1 | Calendar + Offline Group Messaging | إرسال رسالة لحصة أوفلاين خلال <10s |
| T2 | Attendance Viewer | P1 | Real-time attendance sync | تحديث الواجهة خلال <=3s من تسجيل السكرتارية |
| T3 | Grading + Gamification | P1 | Grades dashboard + medals + streak + trend | Top 10 خلال <=2s + تحديث فوري بعد الدرجة |
| T4 | Detailed Reports | P2 | Growth report engine | تقييم آلي بناءً على آخر 3 اختبارات |
| T5 | Financial Monthly Analysis | P1 | Finance dashboard + ledger | جاهز قبل اليوم الخامس شهريًا |
| T6 | Full Access + Delegated Permissions | P1 | RBAC + delegated controls | تعديل صلاحية سكرتير خلال <=30s |
| T7 | UX for Teacher | P1 | Task-optimized UI | تنفيذ المهام الشائعة بدون مساعدة بعد 15 دقيقة |
| T8 | Security | P1 | MFA + Re-auth + Audit logs | منع الحذف الشامل بدون تأكيد + إعادة كلمة السر |
| T9 | Performance | P1 | Query/index/cache optimization | تقارير 500+ طالب خلال <=5s |
| T10 | Leaderboard Automation | P2 | Daily leaderboard job | تحديث كل 24 ساعة مع عرض معايير التكريم |

## Secretary

| ID | Requirement | Priority | Feature/Module | KPI / Acceptance Test |
|---|---|---|---|---|
| S1 | Student/Parent/WhatsApp Data | P1 | Student registry | إدخال طالب + ولي أمر + رابط مجموعة خلال <60s |
| S2 | Offline Attendance Entry | P1 | Quick attendance tool | تسجيل 30 طالب خلال <=60s |
| S3 | Payments & Collection | P1 | Payment log + e-receipt | تسجيل دفعة + إيصال خلال <20s |
| S4 | Parent Reports | P1 | Bulk report generator | إرسال 50 تقرير خلال <5 min |
| S5 | Upload & Assessment Prep | P1 | Controlled upload + question bank entry | رفع ملف 100MB خلال <90s |
| S6 | Schedule Editing | P1 | Official schedule editor | ظهور التعديل للواجهات خلال <=5s |
| S7 | Permission Boundaries | P1 | RBAC enforcement | منع الوصول لمعلومات/صلاحيات المعلم |
| S8 | Data Entry UX | P1 | Keyboard-first attendance UI | التشغيل الكامل من لوحة المفاتيح |

## Student

| ID | Requirement | Priority | Feature/Module | KPI / Acceptance Test |
|---|---|---|---|---|
| ST1 | Structured Content Access | P1 | Unit/lesson content + progress | فتح الدرس + رؤية التقدم خلال <5s |
| ST2 | Quizzes & Assignments | P1 | Quiz engine + submission box | الدرجة الموضوعية خلال <=2s |
| ST3 | Performance Dashboard | P1 | Student analytics + medals/streak | تحديث فوري بعد أي درجة/واجب جديد |
| ST4 | Progress Reports | P2 | Charts over time | رسم بياني شهري خلال <5s |
| ST5 | Mobile UX | P1 | Fully responsive UI | الفيديو والاختبار يعملان على الأجهزة/المتصفحات الرئيسية |
| ST6 | Notifications | P2 | Notification center | إشعار الواجب الجديد خلال <=10s |
| ST7 | Leaderboard View | P1 | Public leaderboard | تحديث كل 24 ساعة |

## Platform / Content / Infra

| ID | Requirement | Priority | Feature/Module | KPI / Acceptance Test |
|---|---|---|---|---|
| P1 | Content Structuring | P1 | Units + drag-drop | 5 دروس + إعادة ترتيب خلال <60s |
| P2 | Media Handling | P1 | Upload + encoding + secure streaming | 500MB جاهز للتشغيل خلال <=5min |
| P3 | Question Bank | P1 | Repository + randomization | اختبار 20 سؤال عشوائي خلال <10s |
| P4 | Global Search | P1 | Search engine + filters | نتائج في <=3s مع 10k+ سجلات |
| P5 | Scalability | P1 | Cloud + caching + autoscaling | 500 مستخدم متزامن، الصفحة الرئيسية <=4s |
| P6 | Security Hardening | P1 | WAF + security audits | منع SQLi + pentest قبل الإطلاق |
| P7 | Notification Hub | P2 | Internal/external notifications APIs | إرسال للجميع خلال <=10s |
| P8 | CMS UX | P2 | Guided authoring workflows | رفع فيديو + تصنيف + اختبار خلال <10min |

## AI Capabilities

| ID | Requirement | Priority | Feature/Module | KPI / Acceptance Test |
|---|---|---|---|---|
| AI1 | Personalized Recommendations | P2 | Recommendation model | 3 توصيات بدقة >=80% |
| AI2 | Predictive Alerts | P2 | Early warning model | إنذار عند هبوط >15% مع FP <10% |
| AI3 | AI Q&A Bot | P2 | Curriculum chatbot | 75% إجابات صحيحة دون تحويل لدعم |
| AI4 | Essay Scoring Assist | P2 | Scoring suggestion engine | تقليل زمن التصحيح >=20% |
| AI5 | AI Performance NFR | P1 | Fast inference pipeline | توليد التوصيات خلال <5s |
| AI6 | Data Privacy | P1 | Data anonymization + approvals | تدريب ببيانات مجهولة + موافقات الصلاحيات |

## Parent

| ID | Requirement | Priority | Feature/Module | KPI / Acceptance Test |
|---|---|---|---|---|
| PR1 | Attendance Follow-up | P1 | Absence alerts + history view | إشعار الغياب خلال <=5 min |
| PR2 | Academic & Financial Follow-up | P1 | Parent summary dashboard | البيانات محدثة خلال <=15 min |
| PR3 | Telegram Bot | P2 | Secure bot integration | استجابة خلال <10s بعد التحقق |
| PR4 | Parent UX | P1 | Simplified interface | الوصول للتقرير الشهري بخطوتين |

---

## Suggested Sprint Breakdown

- **Sprint 1-2**: IAM + RBAC + MFA + Audit + base schemas.
- **Sprint 3-4**: Scheduling + attendance + secretary workflows.
- **Sprint 5-6**: Grading + gamification + student dashboard.
- **Sprint 7-8**: Finance + parent portal + notifications.
- **Sprint 9-10**: CMS + question bank + search.
- **Sprint 11-12**: Hardening, load/security tests, UAT.
- **Phase 2**: AI, Telegram, advanced analytics.

