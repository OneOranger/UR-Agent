def _read_field(item, field_name: str, default=None):
    """
    同时兼容 dict 和对象
    """
    if isinstance(item, dict):
        return item.get(field_name, default)
    return getattr(item, field_name, default)


def evaluate_evidence_coverage(result: dict) -> dict:
    """
    评估 evidence coverage（证据覆盖率）
    """
    insights = result.get("insights", [])

    if not insights:
        return {
            "evaluator_name": "evidence_coverage",
            "score": 0.0,
            "passed": False,
            "detail": {
                "reason": "没有 insights，无法评估证据覆盖率"
            },
        }

    supported_count = 0
    unsupported_insight_ids = []

    for insight in insights:
        supporting_ids = _read_field(insight, "supporting_evidence_ids", [])
        insight_id = _read_field(insight, "insight_id", "")

        if supporting_ids:
            supported_count += 1
        else:
            unsupported_insight_ids.append(insight_id)

    score = supported_count / len(insights)
    passed = score >= 0.8

    return {
        "evaluator_name": "evidence_coverage",
        "score": score,
        "passed": passed,
        "detail": {
            "total_insights": len(insights),
            "supported_insights": supported_count,
            "unsupported_insight_ids": unsupported_insight_ids,
        },
    }