from pydantic import BaseModel, Field


class JourneyStageOutput(BaseModel):
    """
    LLM 输出的单个旅程阶段
    """
    stage_name: str = Field(..., description="阶段名称")
    user_goal: str = Field(..., description="用户目标")
    user_actions: list[str] = Field(default_factory=list, description="用户行为")
    touchpoints: list[str] = Field(default_factory=list, description="接触点")
    pain_points: list[str] = Field(default_factory=list, description="痛点")
    opportunities: list[str] = Field(default_factory=list, description="机会点")
    emotion: str = Field(default="", description="用户情绪")


class JourneyMapOutput(BaseModel):
    """
    LLM 输出的整条旅程图
    """
    overview: str = Field(..., description="旅程总览")
    stages: list[JourneyStageOutput] = Field(default_factory=list, description="阶段列表")