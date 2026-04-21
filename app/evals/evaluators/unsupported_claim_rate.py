def _read_field(item, field_name: str, default=None):
    """
    同时兼容 dict 和对象
    """
    if isinstance(item, dict):
        return item.get(field_name, default)
    return getattr(item, field_name, default)


def evaluate_unsupported_claim_rate(result: dict) -> dict:
    """
    评估 unsupported claim rate（无证据支撑结论率）
    """
    insights = result.get("insights", [])

    if not insights:
        return {
            "evaluator_name": "unsupported_claim_rate",
            "score": 0.0,
            "passed": False,
            "detail": {
                "reason": "没有 insights，无法评估 unsupported claim rate"
            },
        }

    unsupported_count = 0
    unsupported_insight_ids = []

    for insight in insights:
        supporting_ids = _read_field(insight, "supporting_evidence_ids", [])
        insight_id = _read_field(insight, "insight_id", "")

        if not supporting_ids:
            unsupported_count += 1
            unsupported_insight_ids.append(insight_id)

    rate = unsupported_count / len(insights)
    score = 1 - rate
    passed = rate <= 0.2

    return {
        "evaluator_name": "unsupported_claim_rate",
        "score": score,
        "passed": passed,
        "detail": {
            "total_insights": len(insights),
            "unsupported_count": unsupported_count,
            "unsupported_rate": rate,
            "unsupported_insight_ids": unsupported_insight_ids,
        },
    }