from app.domain.models.research_state import ResearchState


def route_after_approval(state: ResearchState) -> str:
    """
    根据人工审核结果决定后续走向。
    """
    if state.approval_decision == "approved":
        return "end"
    return "report_generator"