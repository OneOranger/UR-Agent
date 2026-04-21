import time
from typing import Any

from app.core.logger import setup_logger
from app.observability.trace_store import save_trace_sync

logger = setup_logger()


def log_event(event_name: str, payload: dict[str, Any]) -> None:
    """
    统一日志事件输出函数。

    说明：
    1. 先打印到控制台
    2. 再尝试写入 SQLite 的 trace_records 表
    3. 如果 trace 落库失败，不影响主流程
    """
    logger.info(f"[TRACE] {event_name} | {payload}")

    run_id = payload.get("run_id", "")
    thread_id = payload.get("thread_id", "")

    # 只有有 run_id 或 thread_id 时才尝试落库
    if run_id or thread_id:
        try:
            save_trace_sync(
                run_id=run_id,
                thread_id=thread_id,
                event_name=event_name,
                payload=payload,
            )
        except Exception as e:
            logger.warning(f"[TRACE_DB_FAIL] {event_name} | error={str(e)}")


def now_ms() -> float:
    """
    返回当前时间戳（毫秒）。
    """
    return time.perf_counter() * 1000