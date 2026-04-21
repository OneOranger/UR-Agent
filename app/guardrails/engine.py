from app.domain.models.research_state import ResearchState
from app.domain.models.evidence_item import EvidenceItem
from app.guardrails.input.simulated_data_check import reject_simulated_evidence
from app.guardrails.output.unsupported_claim_check import check_unsupported_claims


class GuardrailError(Exception):
    """
    护栏异常。
    只要违反关键规则，就抛出这个异常。
    """
    pass


class GuardrailEngine:
    """
    护栏总引擎。

    作用：
    1. 统一管理输入护栏
    2. 统一管理输出护栏
    3. 节点代码里不直接写一堆 if 判断，保持整洁
    """

    @staticmethod
    def validate_evidence_before_add(evidence: EvidenceItem) -> None:
        """
        在证据进入正式 evidence_bank 之前做检查。
        """
        if reject_simulated_evidence(evidence):
            raise GuardrailError(
                f"禁止将模拟数据写入正式证据库: {evidence.evidence_id}"
            )

    @staticmethod
    def validate_before_synthesis(state: ResearchState) -> None:
        """
        在生成洞察前做检查。

        规则：
        - 必须至少有 1 条正式证据
        """
        formal_evidence = [
            ev for ev in state.evidence_bank
            if not ev.is_simulated
        ]

        if not formal_evidence:
            raise GuardrailError("没有正式证据，禁止生成洞察。")

    @staticmethod
    def validate_before_publish(state: ResearchState) -> None:
        """
        在输出最终报告前做检查。

        规则：
        - 不允许存在 unsupported claims
        """
        errors = check_unsupported_claims(state)

        if errors:
            raise GuardrailError("；".join(errors))