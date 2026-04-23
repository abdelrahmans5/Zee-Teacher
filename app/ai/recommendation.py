from collections import defaultdict
from app.models import ExamResult


def build_recommendations(results: list[ExamResult]) -> tuple[list[str], float]:
    """Heuristic recommender: picks weakest 3 units by average percentage."""
    if not results:
        return [
            "ابدأ بمراجعة Unit 1 fundamentals",
            "حل 10 أسئلة تدريبية يوميًا",
            "شاهد فيديو المراجعة الأسبوعية",
        ], 0.8

    by_unit: dict[str, list[float]] = defaultdict(list)
    for r in results:
        pct = (r.score / r.max_score) * 100 if r.max_score else 0
        by_unit[r.unit_name].append(pct)

    ranked = sorted(
        ((unit, sum(vals) / len(vals)) for unit, vals in by_unit.items()),
        key=lambda x: x[1],
    )

    weakest = [u for u, _ in ranked[:3]]
    while len(weakest) < 3:
        weakest.append("General Practice")

    recs = [
        f"راجع الدروس الخاصة بـ {weakest[0]} مع حل أسئلة مستوى متوسط",
        f"ركز على نقاط الضعف في {weakest[1]} باستخدام فيديوهات قصيرة",
        f"نفّذ اختبار مصغر في {weakest[2]} خلال 24 ساعة",
    ]
    # Estimated confidence based on sample size (bounded)
    confidence = min(0.95, max(0.8, 0.7 + len(results) * 0.02))
    return recs, confidence
