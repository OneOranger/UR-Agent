from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.theme import Theme
from app.storage.sqlite.models import ThemeORM


class ThemeRepository:
    """
    主题仓库
    负责 themes 表的保存和查询
    """

    async def save_themes(
        self,
        session: AsyncSession,
        run_id: str,
        themes: list[Theme],
    ) -> None:
        """
        批量保存 themes
        先删除该 run_id 的旧数据，再批量插入新数据
        """
        await session.execute(
            delete(ThemeORM).where(ThemeORM.run_id == run_id)
        )

        for item in themes:
            row = ThemeORM(
                theme_id=item.theme_id,
                run_id=run_id,
                name=item.name,
                description=item.description,
                supporting_evidence_ids=",".join(item.supporting_evidence_ids),
                confidence_score=item.confidence_score,
            )
            session.add(row)

        await session.commit()

    async def get_themes_by_run_id(
        self,
        session: AsyncSession,
        run_id: str,
    ) -> list[ThemeORM]:
        """
        根据 run_id 查询所有 themes
        """
        stmt = select(ThemeORM).where(ThemeORM.run_id == run_id)
        result = await session.execute(stmt)
        return list(result.scalars().all())