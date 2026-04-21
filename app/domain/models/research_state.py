from pydantic import BaseModel, Field
from app.domain.models.evidence_item import EvidenceItem
from app.domain.models.insight import Insight
from app.domain.models.report import Report
from app.domain.models.theme import Theme
from app.domain.models.persona import Persona
from app.domain.models.journey_map import JourneyMap
from app.domain.models.recommendation import Recommendation


class ResearchState(BaseModel):
    """
    LangGraph 共享状态对象
    """

    run_id: str = Field(..., description="本次运行ID")
    thread_id: str = Field(default="", description="LangGraph 线程ID")
    user_request: str = Field(..., description="用户原始需求")
    current_stage: str = Field(default="init", description="当前阶段")

    research_goal: str = Field(default="", description="研究目标")
    research_plan: dict = Field(default_factory=dict, description="研究计划")

    evidence_bank: list[EvidenceItem] = Field(default_factory=list, description="证据库")
    themes: list[Theme] = Field(default_factory=list, description="主题列表")
    insights: list[Insight] = Field(default_factory=list, description="洞察列表")
    personas: list[Persona] = Field(default_factory=list, description="画像列表")
    journey_maps: list[JourneyMap] = Field(default_factory=list, description="旅程图列表")
    recommendations: list[Recommendation] = Field(default_factory=list, description="建议列表")
    final_report: Report | None = Field(default=None, description="最终报告")

    pending_approval: bool = Field(default=False, description="是否等待人工审核")
    approval_decision: str = Field(default="", description="人工审核结果")
    approval_comment: str = Field(default="", description="人工审核备注")