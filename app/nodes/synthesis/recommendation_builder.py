from app.domain.models.recommendation import Recommendation
from app.domain.models.recommendation_outputs import RecommendationListOutput
from app.domain.models.research_state import ResearchState
from app.llm.executor import LLMExecutor
from app.llm.prompt_loader import PromptLoader
from app.observability.decorators import trace_node


@trace_node("recommendation_builder")
def recommendation_builder(state: ResearchState) -> ResearchState:
    """
    基于 themes + insights + personas + journey_maps 生成结构化建议
    """
    executor = LLMExecutor()
    prompt_loader = PromptLoader()

    theme_text = "\n\n".join(
        [f"主题{i+1}：{theme.name}\n说明：{theme.description}" for i, theme in enumerate(state.themes)]
    )

    insight_text = "\n\n".join(
        [f"洞察{i+1}：{insight.statement}" for i, insight in enumerate(state.insights)]
    )

    persona_text = "\n\n".join(
        [
            f"画像{i+1}：{persona.name}\n"
            f"摘要：{persona.summary}\n"
            f"目标：{'；'.join(persona.goals)}\n"
            f"痛点：{'；'.join(persona.pain_points)}\n"
            f"行为：{'；'.join(persona.behaviors)}\n"
            f"动机：{'；'.join(persona.motivations)}"
            for i, persona in enumerate(state.personas)
        ]
    )

    journey_text = "\n\n".join(
        [
            f"旅程图{i+1}（对应画像：{jm.persona_name}）\n"
            f"总览：{jm.overview}\n"
            f"阶段：{'；'.join([stage.stage_name for stage in jm.stages])}"
            for i, jm in enumerate(state.journey_maps)
        ]
    )

    prompt = prompt_loader.build_prompt(
        task_name="recommendation_builder",
        variables={
            "theme_text": theme_text,
            "insight_text": insight_text,
            "persona_text": persona_text,
            "journey_text": journey_text,
        }
    )

    result: RecommendationListOutput = executor.invoke_structured(
        prompt=prompt,
        output_model=RecommendationListOutput,
    )

    all_evidence_ids = [ev.evidence_id for ev in state.evidence_bank]

    recommendations = []
    for index, item in enumerate(result.recommendations, start=1):
        recommendation = Recommendation(
            recommendation_id=f"rec_{index}",
            title=item.title,
            description=item.description,
            priority=item.priority,
            rationale=item.rationale,
            related_opportunity_area=item.related_opportunity_area,
            supporting_evidence_ids=all_evidence_ids,
        )
        recommendations.append(recommendation)

    state.recommendations = recommendations
    state.current_stage = "report_generator"
    return state