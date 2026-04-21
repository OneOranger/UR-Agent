def evaluate_recommendation_count_check(result: dict) -> dict:
    """
    评估 recommendation 数量是否合理
    """
    recommendations = result.get("recommendations", [])

    count = len(recommendations)

    if 3 <= count <= 5:
        score = 1.0
        passed = True
    elif count == 2 or count == 6:
        score = 0.6
        passed = False
    else:
        score = 0.0
        passed = False

    return {
        "evaluator_name": "recommendation_count_check",
        "score": score,
        "passed": passed,
        "detail": {
            "recommendation_count": count,
            "expected_range": "3-5",
        },
    }