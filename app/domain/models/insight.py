from pydantic import BaseModel, Field


class Insight(BaseModel):
    """
    洞察对象。
    注意：这里强制要求 supporting_evidence_ids。
    这样就能保证“没有证据，不出洞察”。
    """

    insight_id: str = Field(..., description="洞察唯一ID")
    statement: str = Field(..., description="洞察陈述")
    supporting_evidence_ids: list[str] = Field(
        default_factory=list,
        description="支持该洞察的证据ID列表",
    )
    counter_evidence_ids: list[str] = Field(
        default_factory=list,
        description="反证ID列表",
    )
    confidence_score: float = Field(
        ge=0.0,
        le=1.0,
        description="洞察置信度",
    )
    severity: str = Field(default="medium", description="问题严重度")
    opportunity_area: str = Field(default="", description="对应机会点")