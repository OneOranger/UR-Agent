from pydantic import BaseModel, Field
from app.domain.models.insight import Insight


class Report(BaseModel):
    """
    结构化完整报告对象

    说明：
    - 这是研究最终交付物
    - 第一版先用结构化字段表示完整报告
    - 后面你还可以继续扩展成 Markdown / PDF / DOCX 导出
    """

    title: str = Field(..., description="报告标题")
    background: str = Field(default="", description="项目背景")
    research_goal: str = Field(default="", description="研究目标")
    executive_summary: str = Field(default="", description="执行摘要")

    key_findings: list[str] = Field(default_factory=list, description="关键发现")
    themes_summary: list[str] = Field(default_factory=list, description="主题摘要")
    personas_summary: list[str] = Field(default_factory=list, description="画像摘要")
    journey_summary: list[str] = Field(default_factory=list, description="旅程摘要")

    insights: list[Insight] = Field(default_factory=list, description="关键洞察")
    recommendations: list[str] = Field(default_factory=list, description="建议列表")

    methodology: str = Field(default="", description="研究方法说明")
    limitations: list[str] = Field(default_factory=list, description="局限性")
    next_steps: list[str] = Field(default_factory=list, description="下一步建议")