from dataclasses import dataclass


@dataclass
class GuardrailPolicy:
    """
    护栏策略对象。

    说明：
    - name: 策略名称
    - description: 策略说明
    - enabled: 是否启用
    """
    name: str
    description: str
    enabled: bool = True


# ===== 第一版最关键的 3 条策略 =====

EVIDENCE_REQUIRED_POLICY = GuardrailPolicy(
    name="evidence_required",
    description="没有正式证据，不允许生成洞察。",
    enabled=True,
)

NO_SIMULATED_DATA_IN_FORMAL_EVIDENCE_POLICY = GuardrailPolicy(
    name="no_simulated_data_in_formal_evidence",
    description="模拟数据不能进入正式证据库。",
    enabled=True,
)

NO_UNSUPPORTED_CLAIMS_POLICY = GuardrailPolicy(
    name="no_unsupported_claims",
    description="最终报告中的洞察必须引用正式证据。",
    enabled=True,
)