from pydantic import BaseModel, Field


class Theme(BaseModel):
    """
    主题对象

    在用户研究里，Theme 是从多条 Evidence 中归纳出来的中层结构。
    它比原始证据更抽象，但还没有到最终洞察那么高层。
    """

    theme_id: str = Field(..., description="主题唯一ID")
    name: str = Field(..., description="主题名称")
    description: str = Field(..., description="主题说明")
    supporting_evidence_ids: list[str] = Field(
        default_factory=list,
        description="支撑这个主题的证据ID",
    )
    confidence_score: float = Field(
        ge=0.0,
        le=1.0,
        default=0.8,
        description="主题置信度",
    )