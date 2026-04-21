
from functools import wraps

from app.observability.tracing import log_event, now_ms


def trace_node(node_name: str):
    """
    节点追踪装饰器

    用法：
    @trace_node("clarify_goal")
    def clarify_goal(state):
        ...

    作用：
    1. 记录节点开始
    2. 记录节点结束
    3. 记录节点耗时
    4. 自动打印 run_id / current_stage（如果 state 里有）
    """
    def decorator(func):
        @wraps(func)
        def wrapper(state, *args, **kwargs):
            start_time = now_ms()

            run_id = getattr(state, "run_id", "")
            current_stage = getattr(state, "current_stage", "")
            thread_id = getattr(state, "thread_id", "")

            log_event(
                event_name="node_start",
                payload={
                    "node_name": node_name,
                    "run_id": run_id,
                    "thread_id": thread_id,
                    "current_stage": current_stage,
                },
            )

            result = func(state, *args, **kwargs)

            duration_ms = round(now_ms() - start_time, 2)
            result_stage = getattr(result, "current_stage", "")
            result_thread_id = getattr(result, "thread_id", thread_id)

            log_event(
                event_name="node_end",
                payload={
                    "node_name": node_name,
                    "run_id": run_id,
                    "thread_id": result_thread_id,
                    "current_stage": result_stage,
                    "duration_ms": duration_ms,
                },
            )

            return result

        return wrapper
    return decorator