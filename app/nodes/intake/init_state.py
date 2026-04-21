from uuid import uuid4

from app.domain.models.research_state import ResearchState


def init_state(user_request: str, thread_id: str = "") -> ResearchState:
    """
    初始化整个研究流程的状态。
    这是图的起点节点逻辑。
    """
    return ResearchState(
        run_id=str(uuid4()),
        thread_id=thread_id,
        user_request=user_request,
        current_stage="clarify",
    )
