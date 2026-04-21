import asyncio
from typing import Any

from app.storage.sqlite.db import AsyncSessionLocal
from app.storage.repositories.trace_repo import TraceRepository

trace_repo = TraceRepository()


async def save_trace_async(
    run_id: str,
    thread_id: str,
    event_name: str,
    payload: dict,
) -> None:
    """
    异步保存一条 trace
    """
    async with AsyncSessionLocal() as session:
        await trace_repo.save_trace(
            session=session,
            run_id=run_id,
            thread_id=thread_id,
            event_name=event_name,
            payload=payload,
        )


def save_trace_sync(
    run_id: str,
    thread_id: str,
    event_name: str,
    payload: dict,
) -> None:
    """
    同步包装，方便在普通函数里调用
    注意：在异步上下文中不应使用此函数
    """
    try:
        # 检查是否已经在事件循环中
        loop = asyncio.get_running_loop()
        # 如果在事件循环中，创建任务而不是运行
        loop.create_task(
            save_trace_async(
                run_id=run_id,
                thread_id=thread_id,
                event_name=event_name,
                payload=payload,
            )
        )
    except RuntimeError:
        # 没有运行中的事件循环，可以安全使用 asyncio.run()
        asyncio.run(
            save_trace_async(
                run_id=run_id,
                thread_id=thread_id,
                event_name=event_name,
                payload=payload,
            )
        )