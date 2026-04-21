from app.domain.models.journey_map import JourneyMap, JourneyStage
from app.domain.models.journey_outputs import JourneyMapOutput
from app.domain.models.research_state import ResearchState
from app.llm.executor import LLMExecutor
from app.llm.prompt_loader import PromptLoader
from app.observability.decorators import trace_node


@trace_node("journey_mapper")
def journey_mapper(state: ResearchState) -> ResearchState:
    """
    基于 Persona + Themes + Insights 构建 Journey Map
    """
    if not state.personas:
        state.current_stage = "recommendation_builder"
        return state

    executor = LLMExecutor()
    prompt_loader = PromptLoader()

    persona = state.personas[0]

    persona_text = f"""
画像名称：{persona.name}
画像摘要：{persona.summary}
目标：{'；'.join(persona.goals)}
痛点：{'；'.join(persona.pain_points)}
行为特征：{'；'.join(persona.behaviors)}
动机：{'；'.join(persona.motivations)}
""".strip()

    theme_text = "\n\n".join(
        [f"主题{i+1}：{theme.name}\n说明：{theme.description}" for i, theme in enumerate(state.themes)]
    )

    insight_text = "\n\n".join(
        [f"洞察{i+1}：{insight.statement}" for i, insight in enumerate(state.insights)]
    )

    prompt = prompt_loader.build_prompt(
        task_name="journey_mapper",
        variables={
            "persona_text": persona_text,
            "theme_text": theme_text,
            "insight_text": insight_text,
        }
    )

    result: JourneyMapOutput = executor.invoke_structured(
        prompt=prompt,
        output_model=JourneyMapOutput,
    )

    all_evidence_ids = [ev.evidence_id for ev in state.evidence_bank]

    stages = []
    for item in result.stages:
        stage = JourneyStage(
            stage_name=item.stage_name,
            user_goal=item.user_goal,
            user_actions=item.user_actions,
            touchpoints=item.touchpoints,
            pain_points=item.pain_points,
            opportunities=item.opportunities,
            emotion=item.emotion,
        )
        stages.append(stage)

    journey = JourneyMap(
        journey_id="journey_1",
        persona_name=persona.name,
        overview=result.overview,
        stages=stages,
        supporting_evidence_ids=all_evidence_ids,
    )

    state.journey_maps = [journey]
    state.current_stage = "recommendation_builder"
    return state