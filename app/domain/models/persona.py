from pydantic import BaseModel, Field


class Persona(BaseModel):
    """
    用户画像对象

    说明：
    - Persona 不是单个真实用户
    - 而是基于研究材料归纳出来的一类典型用户
    """

    persona_id: str = Field(..., description="画像ID")
    name: str = Field(..., description="画像名称")
    summary: str = Field(..., description="画像摘要")
    goals: list[str] = Field(default_factory=list, description="目标")
    pain_points: list[str] = Field(default_factory=list, description="痛点")
    behaviors: list[str] = Field(default_factory=list, description="行为特征")
    motivations: list[str] = Field(default_factory=list, description="动机")
    supporting_evidence_ids: list[str] = Field(
        default_factory=list,
        description="支撑该画像的证据ID",
    )