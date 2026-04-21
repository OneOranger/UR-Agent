from langgraph.types import interrupt

from app.domain.models.research_state import ResearchState
from app.guardrails.engine import GuardrailEngine
from app.observability.decorators import trace_node


@trace_node("request_final_approval")
def request_final_approval(state: ResearchState) -> ResearchState:
    """

    在人工审核前，先执行发布前护栏检查。
    如果有 unsupported claims，会直接报错，不允许进入发布流程。

    真正的人类审核节点。

    LangGraph 的 interrupt() 会：
    1. 在这里暂停执行
    2. 把当前状态交给 checkpointer 保存
    3. 把中断载荷返回给外部调用方
    4. 等待外部通过 Command(resume=...) 恢复

    注意：
    interrupt() 返回的值，就是恢复时传入的 resume 值。
    """
    # ===== 发布前做最后一道护栏检查 =====
    GuardrailEngine.validate_before_publish(state)

    state.pending_approval = True
    state.current_stage = "waiting_human_approval"

    approval_payload = {
        "type": "final_report_approval",
        "message": "请审核最终研究报告，决定 approved 或 rejected",
        "report_title": state.final_report.title if state.final_report else "",
        "run_id": state.run_id,
    }

    human_response = interrupt(approval_payload)

    # 当外部用 Command(resume=...) 恢复后，
    # human_response 就会拿到 resume 传入的数据
    if isinstance(human_response, dict):
        state.approval_decision = human_response.get("decision", "")
        state.approval_comment = human_response.get("comment", "")
    else:
        state.approval_decision = str(human_response)

    state.pending_approval = False
    state.current_stage = "approved_or_rejected"

    return state