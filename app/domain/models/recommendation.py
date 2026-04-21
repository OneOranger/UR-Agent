from pydantic import BaseModel, Field


class Recommendation(BaseModel):
    """
    产品建议对象

    说明：
    - recommendation 不是泛泛建议
    - 而是基于研究材料生成的、可以被产品团队执行的建议
    """

    recommendation_id: str = Field(..., description="建议ID")
    title: str = Field(..., description="建议标题")
    description: str = Field(..., description="建议说明")
    priority: str = Field(..., description="优先级：high / medium / low")
    rationale: str = Field(..., description="为什么要做这条建议")
    related_opportunity_area: str = Field(default="", description="对应机会点")
    supporting_evidence_ids: list[str] = Field(
        default_factory=list,
        description="支撑该建议的证据ID",
    )