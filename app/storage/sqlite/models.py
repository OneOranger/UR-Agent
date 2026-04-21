from sqlalchemy import String, Text, Float, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.storage.sqlite.db import Base

class ResearchRunORM(Base):
    """
    研究任务运行表
    """
    __tablename__ = "research_runs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    thread_id: Mapped[str] = mapped_column(String(100), index=True)
    user_request: Mapped[str] = mapped_column(Text)
    current_stage: Mapped[str] = mapped_column(String(100))
    research_goal: Mapped[str] = mapped_column(Text, default="")
    markdown_report_path: Mapped[str] = mapped_column(Text, default="")


class EvidenceORM(Base):
    """
    证据表
    """
    __tablename__ = "evidence_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    evidence_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    run_id: Mapped[str] = mapped_column(String(100), ForeignKey("research_runs.run_id"), index=True)

    source_type: Mapped[str] = mapped_column(String(50))
    source_name: Mapped[str] = mapped_column(String(255))
    raw_excerpt: Mapped[str] = mapped_column(Text)
    normalized_text: Mapped[str] = mapped_column(Text)
    confidence: Mapped[float] = mapped_column(Float)
    is_simulated: Mapped[bool] = mapped_column(Boolean, default=False)
    tags: Mapped[str] = mapped_column(Text, default="")


class ThemeORM(Base):
    """
    主题表
    一条记录代表一个 Theme
    """
    __tablename__ = "themes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    theme_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    run_id: Mapped[str] = mapped_column(String(100), ForeignKey("research_runs.run_id"), index=True)

    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    supporting_evidence_ids: Mapped[str] = mapped_column(Text, default="")
    confidence_score: Mapped[float] = mapped_column(Float)


class InsightORM(Base):
    """
    洞察表
    """
    __tablename__ = "insights"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    insight_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    run_id: Mapped[str] = mapped_column(String(100), ForeignKey("research_runs.run_id"), index=True)

    statement: Mapped[str] = mapped_column(Text)
    supporting_evidence_ids: Mapped[str] = mapped_column(Text, default="")
    counter_evidence_ids: Mapped[str] = mapped_column(Text, default="")
    confidence_score: Mapped[float] = mapped_column(Float)
    severity: Mapped[str] = mapped_column(String(50), default="medium")
    opportunity_area: Mapped[str] = mapped_column(String(255), default="")

class PersonaORM(Base):
    """
    画像表
    """
    __tablename__ = "personas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    persona_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    run_id: Mapped[str] = mapped_column(String(100), ForeignKey("research_runs.run_id"), index=True)

    name: Mapped[str] = mapped_column(String(255))
    summary: Mapped[str] = mapped_column(Text)
    goals: Mapped[str] = mapped_column(Text, default="")
    pain_points: Mapped[str] = mapped_column(Text, default="")
    behaviors: Mapped[str] = mapped_column(Text, default="")
    motivations: Mapped[str] = mapped_column(Text, default="")
    supporting_evidence_ids: Mapped[str] = mapped_column(Text, default="")

class JourneyMapORM(Base):
    """
    旅程图表
    第一版把 stages 直接存成 JSON 字符串
    """
    __tablename__ = "journey_maps"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    journey_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    run_id: Mapped[str] = mapped_column(String(100), ForeignKey("research_runs.run_id"), index=True)

    persona_name: Mapped[str] = mapped_column(String(255))
    overview: Mapped[str] = mapped_column(Text)
    stages_json: Mapped[str] = mapped_column(Text, default="")
    supporting_evidence_ids: Mapped[str] = mapped_column(Text, default="")

class RecommendationORM(Base):
    """
    建议表
    """
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    recommendation_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    run_id: Mapped[str] = mapped_column(String(100), ForeignKey("research_runs.run_id"), index=True)

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    priority: Mapped[str] = mapped_column(String(50))
    rationale: Mapped[str] = mapped_column(Text)
    related_opportunity_area: Mapped[str] = mapped_column(String(255), default="")
    supporting_evidence_ids: Mapped[str] = mapped_column(Text, default="")


class ReportORM(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(String(100), ForeignKey("research_runs.run_id"), unique=True, index=True)

    title: Mapped[str] = mapped_column(String(255))
    background: Mapped[str] = mapped_column(Text, default="")
    research_goal: Mapped[str] = mapped_column(Text, default="")
    executive_summary: Mapped[str] = mapped_column(Text, default="")

    key_findings: Mapped[str] = mapped_column(Text, default="")
    themes_summary: Mapped[str] = mapped_column(Text, default="")
    personas_summary: Mapped[str] = mapped_column(Text, default="")
    journey_summary: Mapped[str] = mapped_column(Text, default="")

    methodology: Mapped[str] = mapped_column(Text, default="")
    recommendations: Mapped[str] = mapped_column(Text, default="")
    limitations: Mapped[str] = mapped_column(Text, default="")
    next_steps: Mapped[str] = mapped_column(Text, default="")


class ApprovalORM(Base):
    """
    审批历史表
    """
    __tablename__ = "approvals"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(String(100), ForeignKey("research_runs.run_id"), index=True)
    thread_id: Mapped[str] = mapped_column(String(100), index=True)

    approval_type: Mapped[str] = mapped_column(String(100), default="final_report")
    decision: Mapped[str] = mapped_column(String(50))
    comment: Mapped[str] = mapped_column(Text, default="")
    stage_before: Mapped[str] = mapped_column(String(100), default="")
    stage_after: Mapped[str] = mapped_column(String(100), default="")


class TraceRecordORM(Base):
    """
    Trace 记录表
    """
    __tablename__ = "trace_records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(String(100), index=True, default="")
    thread_id: Mapped[str] = mapped_column(String(100), index=True, default="")
    event_name: Mapped[str] = mapped_column(String(100), index=True)
    payload_json: Mapped[str] = mapped_column(Text, default="")

class EvalRecordORM(Base):
    """
    评估记录表

    一条记录表示一次 run 在某个 evaluator 上的评分结果
    """
    __tablename__ = "eval_records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(String(100), ForeignKey("research_runs.run_id"), index=True)
    evaluator_name: Mapped[str] = mapped_column(String(100), index=True)
    score: Mapped[float] = mapped_column(Float)
    passed: Mapped[bool] = mapped_column(Boolean, default=False)
    detail_json: Mapped[str] = mapped_column(Text, default="")