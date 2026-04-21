from langgraph.graph import StateGraph, END

from app.domain.models.research_state import ResearchState
from app.graph.checkpoints import get_checkpointer
from app.graph.routing import route_after_approval
from app.nodes.clarify.clarify_goal import clarify_goal
from app.nodes.planning.planner import planner
from app.nodes.ingestion.ingest_uploaded_files import ingest_uploaded_files
from app.nodes.analysis.evidence_validator import evidence_validator
from app.nodes.analysis.theme_extractor import theme_extractor
from app.nodes.synthesis.insight_synthesizer import insight_synthesizer
from app.nodes.synthesis.persona_builder import persona_builder
from app.nodes.synthesis.journey_mapper import journey_mapper
from app.nodes.synthesis.recommendation_builder import recommendation_builder
from app.nodes.reporting.report_generator import report_generator
from app.nodes.reporting.markdown_export import markdown_export
from app.nodes.review.request_final_approval import request_final_approval


def build_graph():
    """
    创建 LangGraph 工作流，并挂上 checkpointer。

    有了 checkpointer 之后：
    - 每一步状态都可以保存
    - interrupt() 才能真正暂停
    - 后续可以通过 thread_id 恢复
    """

    graph = StateGraph(ResearchState)

    graph.add_node("clarify_goal", clarify_goal)
    graph.add_node("planner", planner)
    graph.add_node("ingest_uploaded_files", ingest_uploaded_files)
    graph.add_node("evidence_validator", evidence_validator)
    graph.add_node("theme_extractor", theme_extractor)
    graph.add_node("insight_synthesizer", insight_synthesizer)
    graph.add_node("persona_builder", persona_builder)
    graph.add_node("journey_mapper", journey_mapper)
    graph.add_node("recommendation_builder", recommendation_builder)
    graph.add_node("report_generator", report_generator)
    graph.add_node("markdown_export", markdown_export)
    graph.add_node("request_final_approval", request_final_approval)

    graph.set_entry_point("clarify_goal")

    graph.add_edge("clarify_goal", "planner")
    graph.add_edge("planner", "ingest_uploaded_files")
    graph.add_edge("ingest_uploaded_files", "evidence_validator")
    graph.add_edge("evidence_validator", "theme_extractor")
    graph.add_edge("theme_extractor", "insight_synthesizer")
    graph.add_edge("insight_synthesizer", "persona_builder")
    graph.add_edge("persona_builder", "journey_mapper")
    graph.add_edge("journey_mapper", "recommendation_builder")
    graph.add_edge("recommendation_builder", "report_generator")
    graph.add_edge("report_generator", "markdown_export")
    graph.add_edge("markdown_export", "request_final_approval")

    graph.add_conditional_edges(
        "request_final_approval",
        route_after_approval,
        {
            "end": END,
            "report_generator": "report_generator",
        },
    )

    return graph.compile(checkpointer=get_checkpointer())