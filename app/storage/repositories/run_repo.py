from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.research_state import ResearchState
from app.storage.sqlite.models import ResearchRunORM


class RunRepository:
    """
    研究运行记录仓库
    """

    async def upsert_run(self, session: AsyncSession, state: ResearchState, thread_id: str) -> None:
        """
        新增或更新 run 记录
        """
        stmt = select(ResearchRunORM).where(ResearchRunORM.run_id == state.run_id)
        result = await session.execute(stmt)
        row = result.scalar_one_or_none()

        markdown_report_path = state.research_plan.get("markdown_report_path", "")

        if row is None:
            row = ResearchRunORM(
                run_id=state.run_id,
                thread_id=thread_id,
                user_request=state.user_request,
                current_stage=state.current_stage,
                research_goal=state.research_goal,
                markdown_report_path=markdown_report_path,
            )
            session.add(row)
        else:
            row.thread_id = thread_id
            row.user_request = state.user_request
            row.current_stage = state.current_stage
            row.research_goal = state.research_goal
            row.markdown_report_path = markdown_report_path

        await session.commit()

    async def get_run_by_run_id(self, session: AsyncSession, run_id: str) -> ResearchRunORM | None:
        stmt = select(ResearchRunORM).where(ResearchRunORM.run_id == run_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()