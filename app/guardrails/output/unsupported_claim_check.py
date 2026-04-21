from app.domain.models.research_state import ResearchState


def check_unsupported_claims(state: ResearchState) -> list[str]:
    """
    检查最终输出中是否存在“无证据支持的洞察”。

    返回：
    - 错误消息列表
    - 如果列表为空，说明检查通过

    检查规则：
    1. 每条 insight 必须有 supporting_evidence_ids
    2. supporting_evidence_ids 中的每个 ID，必须存在于正式 evidence_bank 中
    """
    errors = []

    formal_evidence_ids = {
        ev.evidence_id
        for ev in state.evidence_bank
        if not ev.is_simulated
    }

    for insight in state.insights:
        # 规则1：必须有 supporting_evidence_ids
        if not insight.supporting_evidence_ids:
            errors.append(
                f"洞察 {insight.insight_id} 没有 supporting_evidence_ids。"
            )
            continue

        # 规则2：洞察引用的证据必须真实存在
        for evidence_id in insight.supporting_evidence_ids:
            if evidence_id not in formal_evidence_ids:
                errors.append(
                    f"洞察 {insight.insight_id} 引用了不存在或非正式的证据ID: {evidence_id}"
                )

    return errors