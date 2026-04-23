def suggest_essay_score(answer_text: str) -> tuple[float, str]:
    """Simple baseline NLP-free scorer for MVP."""
    words = [w for w in answer_text.split() if w.strip()]
    wc = len(words)

    if wc < 30:
        return 55.0, "الإجابة قصيرة جدًا، تحتاج شرح أكثر وأمثلة."
    if wc < 80:
        return 72.0, "إجابة جيدة مبدئيًا، أضف تفاصيل وروابط بين الأفكار."
    if wc < 140:
        return 84.0, "إجابة قوية ومنظمة، راجع الدقة اللغوية فقط."
    return 92.0, "إجابة ممتازة من حيث العمق والتنظيم."
