def compute_drop_alert(percentages: list[float], threshold: float = 15.0) -> tuple[float, bool]:
    """Compares latest score against personal average of previous values."""
    if len(percentages) < 2:
        return 0.0, False
    latest = percentages[-1]
    prev_avg = sum(percentages[:-1]) / len(percentages[:-1])
    if prev_avg == 0:
        return 0.0, False
    drop_pct = ((prev_avg - latest) / prev_avg) * 100
    return round(drop_pct, 2), drop_pct >= threshold
