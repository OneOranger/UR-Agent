from pydantic import BaseModel, Field


class ClarifiedGoalOutput(BaseModel):
    """
    LLM 输出：澄清后的研究目标
    """
    research_goal: str = Field(..., description="清晰、专业的研究目标")
    target_users: list[str] = Field(default_factory=list, description="目标用户群")
    business_context: str = Field(default="", description="业务背景")
    key_questions: list[str] = Field(default_factory=list, description="关键研究问题")


class ResearchPlanOutput(BaseModel):
    """
    LLM 输出：研究计划
    """
    method: str = Field(..., description="建议采用的研究方法")
    steps: list[str] = Field(default_factory=list, description="执行步骤")
    human_checkpoints: list[str] = Field(default_factory=list, description="人工审核节点")
    risks: list[str] = Field(default_factory=list, description="风险列表")


class InsightDraftOutput(BaseModel):
    """
    LLM 输出：单条洞察草稿
    """
    statement: str = Field(..., description="洞察陈述")
    severity: str = Field(default="medium", description="问题严重度")
    opportunity_area: str = Field(default="", description="机会点")
    confidence_score: float = Field(default=0.7, ge=0.0, le=1.0, description="置信度")


class InsightListOutput(BaseModel):
    """
    LLM 输出：多条洞察
    """
    insights: list[InsightDraftOutput] = Field(default_factory=list, description="洞察列表")