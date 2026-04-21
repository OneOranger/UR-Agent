from app.domain.models.research_state import ResearchState
from app.domain.models.theme import Theme
from app.domain.models.theme_outputs import ThemeListOutput
from app.llm.executor import LLMExecutor
from app.llm.prompt_loader import PromptLoader
from app.observability.decorators import trace_node


@trace_node("theme_extractor")
def theme_extractor(state: ResearchState) -> ResearchState:
    """
    从 evidence_bank 中提取研究主题。

    第一版策略：
    1. 把所有 evidence 文本喂给 LLM
    2. 让 LLM 输出结构化主题
    3. 程序侧为每个主题绑定 supporting_evidence_ids
       （第一版先全部绑定，后面再优化成更精确映射）
    """
    executor = LLMExecutor()
    prompt_loader = PromptLoader()

    evidence_texts_text = "\n\n".join(
        [f"证据{i+1}:\n{ev.normalized_text}" for i, ev in enumerate(state.evidence_bank)]
    )

    prompt = prompt_loader.build_prompt(
        task_name="theme_extractor",
        variables={
            "evidence_texts": evidence_texts_text
        }
    )

    result: ThemeListOutput = executor.invoke_structured(
        prompt=prompt,
        output_model=ThemeListOutput,
    )

    all_evidence_ids = [ev.evidence_id for ev in state.evidence_bank]

    themes = []
    for index, item in enumerate(result.themes, start=1):
        theme = Theme(
            theme_id=f"theme_{index}",
            name=item.name,
            description=item.description,
            supporting_evidence_ids=all_evidence_ids,
            confidence_score=item.confidence_score,
        )
        themes.append(theme)

    state.themes = themes
    state.current_stage = "insight_synthesizer"
    return state