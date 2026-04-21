import json

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.storage.sqlite.models import TraceRecordORM


class TraceRepository:
    """
    Trace 记录仓库
    """

    async def save_trace(
        self,
        session: AsyncSession,
        run_id: str,
        thread_id: str,
        event_name: str,
        payload: dict,
    ) -> None:
        """
        保存一条 trace 事件
        """
        row = TraceRecordORM(
            run_id=run_id,
            thread_id=thread_id,
            event_name=event_name,
            payload_json=json.dumps(payload, ensure_ascii=False),
        )
        session.add(row)
        await session.commit()

    async def get_traces_by_run_id(
        self,
        session: AsyncSession,
        run_id: str,
    ) -> list[TraceRecordORM]:
        """
        根据 run_id 查询 trace 记录
        """
        stmt = select(TraceRecordORM).where(TraceRecordORM.run_id == run_id)
        result = await session.execute(stmt)
        return list(result.scalars().all())