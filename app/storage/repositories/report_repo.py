from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.report import Report
from app.storage.sqlite.models import ReportORM


class ReportRepository:
    """
    报告仓库
    """

    async def save_report(
        self,
        session: AsyncSession,
        run_id: str,
        report: Report | None,
    ) -> None:
        """
        保存结构化报告
        """
        if report is None:
            return

        stmt = select(ReportORM).where(ReportORM.run_id == run_id)
        result = await session.execute(stmt)
        row = result.scalar_one_or_none()

        key_findings_text = "\n".join(report.key_findings)
        themes_summary_text = "\n".join(report.themes_summary)
        personas_summary_text = "\n".join(report.personas_summary)
        journey_summary_text = "\n".join(report.journey_summary)
        recommendations_text = "\n".join(report.recommendations)
        limitations_text = "\n".join(report.limitations)
        next_steps_text = "\n".join(report.next_steps)

        if row is None:
            row = ReportORM(
                run_id=run_id,
                title=report.title,
                background=report.background,
                research_goal=report.research_goal,
                executive_summary=report.executive_summary,
                key_findings=key_findings_text,
                themes_summary=themes_summary_text,
                personas_summary=personas_summary_text,
                journey_summary=journey_summary_text,
                methodology=report.methodology,
                recommendations=recommendations_text,
                limitations=limitations_text,
                next_steps=next_steps_text,
            )
            session.add(row)
        else:
            row.title = report.title
            row.background = report.background
            row.research_goal = report.research_goal
            row.executive_summary = report.executive_summary
            row.key_findings = key_findings_text
            row.themes_summary = themes_summary_text
            row.personas_summary = personas_summary_text
            row.journey_summary = journey_summary_text
            row.methodology = report.methodology
            row.recommendations = recommendations_text
            row.limitations = limitations_text
            row.next_steps = next_steps_text

        await session.commit()