from app.domain.models.insight import Insight
from app.domain.models.llm_outputs import InsightListOutput
from app.domain.models.research_state import ResearchState
from app.llm.executor import LLMExecutor
from app.observability.decorators import trace_node


@trace_node("insight_synthesizer")
def insight_synthesizer(state: ResearchState) -> ResearchState:
    """
    基于 themes 生成洞察，而不是直接基于原始 evidence。

    这样更符合真实用户研究流程：
    evidence -> themes -> insights
    """
    executor = LLMExecutor()

    theme_text = "\n\n".join(
        [
            f"主题{i+1}：{theme.name}\n说明：{theme.description}"
            for i, theme in enumerate(state.themes)
        ]
    )

    prompt = f"""
你是专业的用户研究洞察专家。
请基于以下研究主题，提炼结构化洞察。

研究主题：
{theme_text}

要求：
1. 洞察要比主题更高一层，总结出用户行为、痛点或需求模式
2. 不要编造与主题无关的内容
3. severity 只能是 low / medium / high
4. confidence_score 在 0 到 1 之间
5. 输出 2 到 5 条洞察
""".strip()

    result: InsightListOutput = executor.invoke_structured(
        prompt=prompt,
        output_model=InsightListOutput,
    )

    all_evidence_ids = [ev.evidence_id for ev in state.evidence_bank]

    insights = []
    for index, item in enumerate(result.insights, start=1):
        insight = Insight(
            insight_id=f"ins_{index}",
            statement=item.statement,
            supporting_evidence_ids=all_evidence_ids,
            counter_evidence_ids=[],
            confidence_score=item.confidence_score,
            severity=item.severity,
            opportunity_area=item.opportunity_area,
        )
        insights.append(insight)

    state.insights = insights
    state.current_stage = "persona_builder"
    return state