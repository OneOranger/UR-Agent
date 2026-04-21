from app.domain.models.evidence_item import EvidenceItem


def reject_simulated_evidence(evidence: EvidenceItem) -> bool:
    """
    检查一条证据是否应该被拒绝进入正式证据库。

    返回：
    - True: 拒绝
    - False: 允许进入正式证据库

    规则：
    - 只要 is_simulated=True，就拒绝
    - 或者 source_type == "simulated"，也拒绝
    """
    if evidence.is_simulated:
        return True

    if evidence.source_type == "simulated":
        return True

    return False