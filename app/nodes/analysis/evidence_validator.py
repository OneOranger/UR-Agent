from app.domain.models.research_state import ResearchState
from app.guardrails.engine import GuardrailEngine
from app.observability.decorators import trace_node


@trace_node("evidence_validator")
def evidence_validator(state: ResearchState) -> ResearchState:
    """
    在进入洞察生成前，检查证据是否足够。
    """
    GuardrailEngine.validate_before_synthesis(state)

    state.current_stage = "theme_extractor"
    return state