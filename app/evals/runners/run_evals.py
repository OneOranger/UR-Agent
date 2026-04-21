from app.evals.evaluators.evidence_coverage import evaluate_evidence_coverage
from app.evals.evaluators.unsupported_claim_rate import evaluate_unsupported_claim_rate
from app.evals.evaluators.recommendation_count_check import evaluate_recommendation_count_check


def run_all_evaluators(result: dict) -> list[dict]:
    """
    运行所有评估器，并返回评估结果列表
    """
    outputs = []

    outputs.append(evaluate_evidence_coverage(result))
    outputs.append(evaluate_unsupported_claim_rate(result))
    outputs.append(evaluate_recommendation_count_check(result))

    return outputs