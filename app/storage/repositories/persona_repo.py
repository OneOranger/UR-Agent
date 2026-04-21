from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.persona import Persona
from app.storage.sqlite.models import PersonaORM


class PersonaRepository:
    """
    Persona 仓库
    """

    async def save_personas(
        self,
        session: AsyncSession,
        run_id: str,
        personas: list[Persona],
    ) -> None:
        """
        批量保存 personas
        先删除该 run_id 的旧数据，再批量插入新数据
        """
        await session.execute(
            delete(PersonaORM).where(PersonaORM.run_id == run_id)
        )

        for item in personas:
            row = PersonaORM(
                persona_id=item.persona_id,
                run_id=run_id,
                name=item.name,
                summary=item.summary,
                goals=",".join(item.goals),
                pain_points=",".join(item.pain_points),
                behaviors=",".join(item.behaviors),
                motivations=",".join(item.motivations),
                supporting_evidence_ids=",".join(item.supporting_evidence_ids),
            )
            session.add(row)

        await session.commit()

    async def get_personas_by_run_id(
        self,
        session: AsyncSession,
        run_id: str,
    ) -> list[PersonaORM]:
        stmt = select(PersonaORM).where(PersonaORM.run_id == run_id)
        result = await session.execute(stmt)
        return list(result.scalars().all())