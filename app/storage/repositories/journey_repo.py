import json

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.journey_map import JourneyMap
from app.storage.sqlite.models import JourneyMapORM


class JourneyRepository:
    """
    Journey Map 仓库
    """

    async def save_journey_maps(
        self,
        session: AsyncSession,
        run_id: str,
        journey_maps: list[JourneyMap],
    ) -> None:
        """
        批量保存 journey maps
        先删除该 run_id 的旧数据，再批量插入新数据
        """
        await session.execute(
            delete(JourneyMapORM).where(JourneyMapORM.run_id == run_id)
        )

        for item in journey_maps:
            stages_json = json.dumps(
                [stage.model_dump() for stage in item.stages],
                ensure_ascii=False,
            )

            row = JourneyMapORM(
                journey_id=item.journey_id,
                run_id=run_id,
                persona_name=item.persona_name,
                overview=item.overview,
                stages_json=stages_json,
                supporting_evidence_ids=",".join(item.supporting_evidence_ids),
            )
            session.add(row)

        await session.commit()

    async def get_journey_maps_by_run_id(
        self,
        session: AsyncSession,
        run_id: str,
    ) -> list[JourneyMapORM]:
        stmt = select(JourneyMapORM).where(JourneyMapORM.run_id == run_id)
        result = await session.execute(stmt)
        return list(result.scalars().all())