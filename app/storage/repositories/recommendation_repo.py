from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.recommendation import Recommendation
from app.storage.sqlite.models import RecommendationORM


class RecommendationRepository:
    """
    Recommendation 仓库
    """

    async def save_recommendations(
        self,
        session: AsyncSession,
        run_id: str,
        recommendations: list[Recommendation],
    ) -> None:
        """
        批量保存 recommendations
        先删除该 run_id 的旧数据，再批量插入新数据
        """
        await session.execute(
            delete(RecommendationORM).where(RecommendationORM.run_id == run_id)
        )

        for item in recommendations:
            row = RecommendationORM(
                recommendation_id=item.recommendation_id,
                run_id=run_id,
                title=item.title,
                description=item.description,
                priority=item.priority,
                rationale=item.rationale,
                related_opportunity_area=item.related_opportunity_area,
                supporting_evidence_ids=",".join(item.supporting_evidence_ids),
            )
            session.add(row)

        await session.commit()

    async def get_recommendations_by_run_id(
        self,
        session: AsyncSession,
        run_id: str,
    ) -> list[RecommendationORM]:
        stmt = select(RecommendationORM).where(RecommendationORM.run_id == run_id)
        result = await session.execute(stmt)
        return list(result.scalars().all())