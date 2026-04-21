from pydantic import BaseModel, Field


class JourneyStage(BaseModel):
    """
    用户旅程中的单个阶段
    """
    stage_name: str = Field(..., description="阶段名称")
    user_goal: str = Field(..., description="这个阶段用户想达成什么")
    user_actions: list[str] = Field(default_factory=list, description="这个阶段用户会做什么")
    touchpoints: list[str] = Field(default_factory=list, description="接触点")
    pain_points: list[str] = Field(default_factory=list, description="痛点")
    opportunities: list[str] = Field(default_factory=list, description="机会点")
    emotion: str = Field(default="", description="用户情绪")


class JourneyMap(BaseModel):
    """
    用户旅程图对象
    第一版先按 persona 生成一条旅程图
    """
    journey_id: str = Field(..., description="旅程图ID")
    persona_name: str = Field(..., description="对应画像名称")
    overview: str = Field(..., description="旅程总览")
    stages: list[JourneyStage] = Field(default_factory=list, description="阶段列表")
    supporting_evidence_ids: list[str] = Field(default_factory=list, description="支撑该旅程图的证据ID")