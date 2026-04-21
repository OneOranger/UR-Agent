from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.insight import Insight
from app.storage.sqlite.models import InsightORM


class InsightRepository:
    """
    洞察仓库
    负责 insights 表的保存和查询
    """

    async def save_insights(
        self,
        session: AsyncSession,
        run_id: str,
        insights: list[Insight],
    ) -> None:
        """
        批量保存洞察。
        先删除该 run_id 的旧数据，再批量插入新数据
        """
        await session.execute(
            delete(InsightORM).where(InsightORM.run_id == run_id)
        )

        for item in insights:
            row = InsightORM(
                insight_id=item.insight_id,
                run_id=run_id,
                statement=item.statement,
                supporting_evidence_ids=",".join(item.supporting_evidence_ids),
                counter_evidence_ids=",".join(item.counter_evidence_ids),
                confidence_score=item.confidence_score,
                severity=item.severity,
                opportunity_area=item.opportunity_area,
            )
            session.add(row)

        await session.commit()

    async def get_insights_by_run_id(
        self,
        session: AsyncSession,
        run_id: str,
    ) -> list[InsightORM]:
        """
        根据 run_id 查询该 run 下的所有洞察
        """
        stmt = select(InsightORM).where(InsightORM.run_id == run_id)
        result = await session.execute(stmt)
        return list(result.scalars().all())