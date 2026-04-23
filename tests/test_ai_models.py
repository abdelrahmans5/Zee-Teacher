from app.ai.risk import compute_drop_alert
from app.ai.essay import suggest_essay_score


def test_drop_alert_triggered():
    drop, high = compute_drop_alert([90, 88, 85, 60])
    assert drop > 15
    assert high is True


def test_essay_score_long_answer():
    text = "word " * 120
    score, feedback = suggest_essay_score(text)
    assert score >= 84
    assert isinstance(feedback, str)
