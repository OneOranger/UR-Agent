import json

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.storage.sqlite.models import EvalRecordORM


class EvalRepository:
    """
    评估记录仓库
    """

    async def save_eval_record(
        self,
        session: AsyncSession,
        run_id: str,
        evaluator_name: str,
        score: float,
        passed: bool,
        detail: dict,
    ) -> None:
        """
        保存一条评估记录

        第一版策略：
        - 同一个 run_id + evaluator_name 如果已存在，就更新
        - 否则插入
        """
        stmt = select(EvalRecordORM).where(
            EvalRecordORM.run_id == run_id,
            EvalRecordORM.evaluator_name == evaluator_name,
        )
        result = await session.execute(stmt)
        row = result.scalar_one_or_none()

        detail_json = json.dumps(detail, ensure_ascii=False)

        if row is None:
            row = EvalRecordORM(
                run_id=run_id,
                evaluator_name=evaluator_name,
                score=score,
                passed=passed,
                detail_json=detail_json,
            )
            session.add(row)
        else:
            row.score = score
            row.passed = passed
            row.detail_json = detail_json

        await session.commit()

    async def get_eval_records_by_run_id(
        self,
        session: AsyncSession,
        run_id: str,
    ) -> list[EvalRecordORM]:
        """
        查询某个 run 的全部评估记录
        """
        stmt = select(EvalRecordORM).where(EvalRecordORM.run_id == run_id)
        result = await session.execute(stmt)
        return list(result.scalars().all())