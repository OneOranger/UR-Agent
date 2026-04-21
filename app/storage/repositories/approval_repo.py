from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.storage.sqlite.models import ApprovalORM


class ApprovalRepository:
    """
    审批历史仓库
    """

    async def save_approval(
        self,
        session: AsyncSession,
        run_id: str,
        thread_id: str,
        approval_type: str,
        decision: str,
        comment: str,
        stage_before: str,
        stage_after: str,
    ) -> None:
        """
        保存一次审批记录
        """
        row = ApprovalORM(
            run_id=run_id,
            thread_id=thread_id,
            approval_type=approval_type,
            decision=decision,
            comment=comment,
            stage_before=stage_before,
            stage_after=stage_after,
        )
        session.add(row)
        await session.commit()

    async def get_approvals_by_run_id(
        self,
        session: AsyncSession,
        run_id: str,
    ) -> list[ApprovalORM]:
        """
        根据 run_id 查询审批历史
        """
        stmt = select(ApprovalORM).where(ApprovalORM.run_id == run_id)
        result = await session.execute(stmt)
        return list(result.scalars().all())