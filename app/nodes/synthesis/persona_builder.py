from app.domain.models.persona import Persona
from app.domain.models.persona_outputs import PersonaListOutput
from app.domain.models.research_state import ResearchState
from app.llm.executor import LLMExecutor
from app.llm.prompt_loader import PromptLoader
from app.observability.decorators import trace_node


@trace_node("persona_builder")
def persona_builder(state: ResearchState) -> ResearchState:
    """
    基于 themes + insights + evidence 构建 Persona
    """
    executor = LLMExecutor()
    prompt_loader = PromptLoader()

    theme_text = "\n\n".join(
        [f"主题{i+1}：{theme.name}\n说明：{theme.description}" for i, theme in enumerate(state.themes)]
    )

    insight_text = "\n\n".join(
        [f"洞察{i+1}：{insight.statement}" for i, insight in enumerate(state.insights)]
    )

    evidence_texts = "\n\n".join(
        [f"证据{i+1}:\n{ev.normalized_text}" for i, ev in enumerate(state.evidence_bank)]
    )

    prompt = prompt_loader.build_prompt(
        task_name="persona_builder",
        variables={
            "theme_text": theme_text,
            "insight_text": insight_text,
            "evidence_texts": evidence_texts,
        }
    )

    result: PersonaListOutput = executor.invoke_structured(
        prompt=prompt,
        output_model=PersonaListOutput,
    )

    all_evidence_ids = [ev.evidence_id for ev in state.evidence_bank]

    personas = []
    for index, item in enumerate(result.personas, start=1):
        persona = Persona(
            persona_id=f"persona_{index}",
            name=item.name,
            summary=item.summary,
            goals=item.goals,
            pain_points=item.pain_points,
            behaviors=item.behaviors,
            motivations=item.motivations,
            supporting_evidence_ids=all_evidence_ids,
        )
        personas.append(persona)

    state.personas = personas
    state.current_stage = "journey_mapper"
    return state