from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.evidence_item import EvidenceItem
from app.storage.sqlite.models import EvidenceORM


class EvidenceRepository:
    """
    证据仓库
    """

    async def save_evidence_items(
        self,
        session: AsyncSession,
        run_id: str,
        evidence_items: list[EvidenceItem],
    ) -> None:
        """
        批量保存证据
        先删除该 run_id 的旧数据，再批量插入新数据
        """
        await session.execute(
            delete(EvidenceORM).where(EvidenceORM.run_id == run_id)
        )

        for item in evidence_items:
            row = EvidenceORM(
                evidence_id=item.evidence_id,
                run_id=run_id,
                source_type=item.source_type,
                source_name=item.source_name,
                raw_excerpt=item.raw_excerpt,
                normalized_text=item.normalized_text,
                confidence=item.confidence,
                is_simulated=item.is_simulated,
                tags=",".join(item.tags),
            )
            session.add(row)

        await session.commit()