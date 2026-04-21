from pydantic import BaseModel, Field


class RecommendationDraftOutput(BaseModel):
    """
    单条建议草稿
    """
    title: str = Field(..., description="建议标题")
    description: str = Field(..., description="建议说明")
    priority: str = Field(..., description="优先级：high / medium / low")
    rationale: str = Field(..., description="建议原因")
    related_opportunity_area: str = Field(default="", description="机会点")


class RecommendationListOutput(BaseModel):
    """
    建议列表输出
    """
    recommendations: list[RecommendationDraftOutput] = Field(
        default_factory=list,
        description="建议列表",
    )