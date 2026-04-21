from app.domain.models.research_state import ResearchState
from app.domain.models.llm_outputs import ClarifiedGoalOutput
from app.llm.executor import LLMExecutor
from app.llm.prompt_loader import PromptLoader
from app.observability.decorators import trace_node


@trace_node("clarify_goal")
def clarify_goal(state: ResearchState) -> ResearchState:
    """
    使用 PromptLoader + LLM 把用户原始需求转成专业研究目标。
    """
    executor = LLMExecutor()
    prompt_loader = PromptLoader()

    prompt = prompt_loader.build_prompt(
        task_name="clarify_goal",
        variables={
            "user_request": state.user_request,
        }
    )

    result: ClarifiedGoalOutput = executor.invoke_structured(
        prompt=prompt,
        output_model=ClarifiedGoalOutput,
    )

    state.research_goal = result.research_goal
    state.current_stage = "planner"

    return state