from pydantic import BaseModel, Field


class PersonaDraftOutput(BaseModel):
    """
    单个 Persona 草稿
    """
    name: str = Field(..., description="画像名称")
    summary: str = Field(..., description="画像摘要")
    goals: list[str] = Field(default_factory=list, description="目标")
    pain_points: list[str] = Field(default_factory=list, description="痛点")
    behaviors: list[str] = Field(default_factory=list, description="行为特征")
    motivations: list[str] = Field(default_factory=list, description="动机")


class PersonaListOutput(BaseModel):
    """
    Persona 列表输出
    第一版先允许 1-3 个
    """
    personas: list[PersonaDraftOutput] = Field(default_factory=list, description="画像列表")