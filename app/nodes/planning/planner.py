from app.domain.models.research_state import ResearchState
from app.domain.models.llm_outputs import ResearchPlanOutput
from app.llm.executor import LLMExecutor
from app.llm.prompt_loader import PromptLoader
from app.observability.decorators import trace_node


@trace_node("planner")
def planner(state: ResearchState) -> ResearchState:
    """
    使用 PromptLoader + LLM 生成结构化研究计划。
    """
    executor = LLMExecutor()
    prompt_loader = PromptLoader()

    prompt = prompt_loader.build_prompt(
        task_name="planner",
        variables={
            "user_request": state.user_request,
            "research_goal": state.research_goal,
        }
    )

    result: ResearchPlanOutput = executor.invoke_structured(
        prompt=prompt,
        output_model=ResearchPlanOutput,
    )

    state.research_plan = {
        "method": result.method,
        "steps": result.steps,
        "human_checkpoints": result.human_checkpoints,
        "risks": result.risks,
    }
    state.current_stage = "ingest_uploaded_files"

    return state