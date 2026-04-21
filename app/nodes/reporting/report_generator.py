from app.domain.models.report import Report
from app.domain.models.research_state import ResearchState
from app.observability.decorators import trace_node


@trace_node("report_generator")
def report_generator(state: ResearchState) -> ResearchState:
    """
    基于当前研究状态生成结构化完整报告
    """

    theme_names = [theme.name for theme in state.themes]
    persona_names = [persona.name for persona in state.personas]
    journey_persona_names = [jm.persona_name for jm in state.journey_maps]
    recommendation_titles = [rec.title for rec in state.recommendations]

    key_findings = [insight.statement for insight in state.insights]

    themes_summary = [
        f"{theme.name}：{theme.description}"
        for theme in state.themes
    ]

    personas_summary = [
        f"{persona.name}：{persona.summary}"
        for persona in state.personas
    ]

    journey_summary = [
        f"{jm.persona_name} 的旅程图包含 {len(jm.stages)} 个阶段，概览：{jm.overview}"
        for jm in state.journey_maps
    ]

    limitations = [
        "当前样本量较小，研究结论仍需更多真实用户数据验证。",
        "当前证据主要来自已上传文本材料，数据来源还不够丰富。",
    ]

    next_steps = [
        "补充更多真实用户访谈和问卷数据，提升结论可靠性。",
        "针对高优先级建议设计可验证的产品方案。",
        "继续扩展 Persona 与 Journey Map 的细分程度。",
    ]

    executive_summary = (
        f"本次研究围绕“{state.user_request}”展开，"
        f"识别出的核心主题包括：{'；'.join(theme_names) if theme_names else '暂无主题'}。"
        f"提炼出的典型用户画像包括：{'；'.join(persona_names) if persona_names else '暂无画像'}。"
        f"已生成旅程图的画像包括：{'；'.join(journey_persona_names) if journey_persona_names else '暂无旅程图'}。"
        f"最终形成 {len(recommendation_titles)} 条产品建议。"
    )

    state.final_report = Report(
        title="User Research Report",
        background=f"研究背景：{state.user_request}",
        research_goal=state.research_goal,
        executive_summary=executive_summary,
        key_findings=key_findings,
        themes_summary=themes_summary,
        personas_summary=personas_summary,
        journey_summary=journey_summary,
        insights=state.insights,
        recommendations=recommendation_titles,
        methodology="Desk research + uploaded file analysis + theme extraction + persona building + journey mapping + recommendation building",
        limitations=limitations,
        next_steps=next_steps,
    )

    state.current_stage = "markdown_export"
    return state