import asyncio
import json
import logging
from uuid import uuid4
from typing import Any

from fastapi import APIRouter, HTTPException
from langgraph.types import Command
from sqlalchemy import select

from app.domain.schemas.api_requests import CreateResearchRunRequest
from app.domain.schemas.approval import ResumeResearchRunRequest
from app.graph.builder import build_graph
from app.guardrails.engine import GuardrailError
from app.nodes.intake.init_state import init_state
from app.observability.tracing import log_event
from app.storage.sqlite.db import AsyncSessionLocal
from app.storage.repositories.run_repo import RunRepository
from app.storage.repositories.evidence_repo import EvidenceRepository
from app.storage.repositories.theme_repo import ThemeRepository
from app.storage.repositories.insight_repo import InsightRepository
from app.storage.repositories.persona_repo import PersonaRepository
from app.storage.repositories.journey_repo import JourneyRepository
from app.storage.repositories.recommendation_repo import RecommendationRepository
from app.storage.repositories.report_repo import ReportRepository
from app.storage.repositories.approval_repo import ApprovalRepository
from app.storage.repositories.trace_repo import TraceRepository
from app.storage.sqlite.models import (
    ResearchRunORM,
    EvidenceORM,
    ThemeORM,
    InsightORM,
    PersonaORM,
    JourneyMapORM,
    RecommendationORM,
    ReportORM,
)
from app.evals.runners.run_evals import run_all_evaluators
from app.storage.repositories.eval_repo import EvalRepository
from app.storage.sqlite.models import EvalRecordORM


router = APIRouter(prefix="/research", tags=["research"])

logger = logging.getLogger(__name__)

# 第一版先把 graph 放在模块级，保证内存 checkpointer 能持续存在
app_graph = build_graph()

run_repo = RunRepository()
evidence_repo = EvidenceRepository()
theme_repo = ThemeRepository()
insight_repo = InsightRepository()
persona_repo = PersonaRepository()
journey_repo = JourneyRepository()
recommendation_repo = RecommendationRepository()
report_repo = ReportRepository()
approval_repo = ApprovalRepository()
trace_repo = TraceRepository()
eval_repo = EvalRepository()

def normalize_graph_result(raw_result: Any) -> tuple[dict, list[dict]]:
    """
    把 LangGraph 的返回值统一转成：
    1. state_dict: 纯 dict 状态
    2. interrupts: 纯 JSON 可序列化的中断列表

    兼容两种情况：
    - v1: invoke() 返回 dict，interrupt 在 __interrupt__
    - v2: invoke() 返回 GraphOutput，state 在 .value，interrupt 在 .interrupts
    """
    interrupts: list[dict] = []

    # ===== v2 风格：GraphOutput =====
    if hasattr(raw_result, "value") and hasattr(raw_result, "interrupts"):
        state_dict = raw_result.value if isinstance(raw_result.value, dict) else dict(raw_result.value)

        raw_interrupts = raw_result.interrupts or []
        for item in raw_interrupts:
            interrupts.append({
                "value": getattr(item, "value", str(item))
            })

        return state_dict, interrupts

    # ===== v1 风格：dict + __interrupt__ =====
    if isinstance(raw_result, dict):
        state_dict = dict(raw_result)

        raw_interrupts = state_dict.pop("__interrupt__", None)
        if raw_interrupts:
            for item in raw_interrupts:
                interrupts.append({
                    "value": getattr(item, "value", str(item))
                })

        return state_dict, interrupts

    # ===== 兜底 =====
    return {"raw_result": str(raw_result)}, interrupts

async def persist_state(thread_id: str, result: dict) -> None:
    """
    把图运行结果持久化到 SQLite。

    注意：
    - 这里只接收"纯状态 dict"
    - 不接收 __interrupt__ 或 GraphOutput
    """
    logger.info(
        f"persist_state called: run_id={result.get('run_id', 'N/A')}, "
        f"evidence_bank={len(result.get('evidence_bank', []))}, "
        f"themes={len(result.get('themes', []))}, "
        f"insights={len(result.get('insights', []))}, "
        f"personas={len(result.get('personas', []))}, "
        f"journey_maps={len(result.get('journey_maps', []))}, "
        f"recommendations={len(result.get('recommendations', []))}, "
        f"final_report={'Yes' if result.get('final_report') else 'No'}"
    )

    # 将 Pydantic 对象转为 dict，确保 ResearchState(**result) 能正确处理
    for field_name in ["evidence_bank", "themes", "insights", "personas", "journey_maps", "recommendations"]:
        items = result.get(field_name)
        if items and isinstance(items, list):
            result[field_name] = [
                item.model_dump() if hasattr(item, "model_dump") else item
                for item in items
            ]
    if result.get("final_report") and hasattr(result["final_report"], "model_dump"):
        result["final_report"] = result["final_report"].model_dump()

    async with AsyncSessionLocal() as session:
        from app.domain.models.research_state import ResearchState
        from app.domain.models.evidence_item import EvidenceItem
        from app.domain.models.theme import Theme
        from app.domain.models.insight import Insight
        from app.domain.models.persona import Persona
        from app.domain.models.journey_map import JourneyMap
        from app.domain.models.recommendation import Recommendation
        from app.domain.models.report import Report

        state_obj = ResearchState(**result)
        await run_repo.upsert_run(session, state_obj, thread_id)

        if result.get("evidence_bank"):
            try:
                evidence_items = [
                    EvidenceItem(**item) if isinstance(item, dict) else item
                    for item in result["evidence_bank"]
                ]
                await evidence_repo.save_evidence_items(
                    session=session,
                    run_id=result["run_id"],
                    evidence_items=evidence_items,
                )
            except Exception as e:
                logger.error(f"保存证据失败 (run_id={result.get('run_id')}): {e}", exc_info=True)

        if result.get("themes"):
            try:
                themes = [
                    Theme(**item) if isinstance(item, dict) else item
                    for item in result["themes"]
                ]
                await theme_repo.save_themes(
                    session=session,
                    run_id=result["run_id"],
                    themes=themes,
                )
            except Exception as e:
                logger.error(f"保存主题失败 (run_id={result.get('run_id')}): {e}", exc_info=True)

        if result.get("insights"):
            try:
                insights = [
                    Insight(**item) if isinstance(item, dict) else item
                    for item in result["insights"]
                ]
                await insight_repo.save_insights(
                    session=session,
                    run_id=result["run_id"],
                    insights=insights,
                )
            except Exception as e:
                logger.error(f"保存洞察失败 (run_id={result.get('run_id')}): {e}", exc_info=True)

        if result.get("personas"):
            try:
                personas = [
                    Persona(**item) if isinstance(item, dict) else item
                    for item in result["personas"]
                ]
                await persona_repo.save_personas(
                    session=session,
                    run_id=result["run_id"],
                    personas=personas,
                )
            except Exception as e:
                logger.error(f"保存画像失败 (run_id={result.get('run_id')}): {e}", exc_info=True)

        if result.get("journey_maps"):
            try:
                journey_maps = [
                    JourneyMap(**item) if isinstance(item, dict) else item
                    for item in result["journey_maps"]
                ]
                await journey_repo.save_journey_maps(
                    session=session,
                    run_id=result["run_id"],
                    journey_maps=journey_maps,
                )
            except Exception as e:
                logger.error(f"保存旅程图失败 (run_id={result.get('run_id')}): {e}", exc_info=True)

        if result.get("recommendations"):
            try:
                recommendations = [
                    Recommendation(**item) if isinstance(item, dict) else item
                    for item in result["recommendations"]
                ]
                await recommendation_repo.save_recommendations(
                    session=session,
                    run_id=result["run_id"],
                    recommendations=recommendations,
                )
            except Exception as e:
                logger.error(f"保存建议失败 (run_id={result.get('run_id')}): {e}", exc_info=True)

        if result.get("final_report"):
            try:
                report_obj = (
                    Report(**result["final_report"])
                    if isinstance(result["final_report"], dict)
                    else result["final_report"]
                )
                await report_repo.save_report(
                    session=session,
                    run_id=result["run_id"],
                    report=report_obj,
                )
            except Exception as e:
                logger.error(f"保存报告失败 (run_id={result.get('run_id')}): {e}", exc_info=True)

async def persist_evals(run_id: str, result: dict) -> None:
    """
    运行评估器并把结果写入数据库

    说明：
    - 先把 result 中的 Pydantic 对象尽量转成纯 dict
    - 避免 evaluator 里出现对象/字典混用问题
    """
    normalized_result = {}

    for key, value in result.items():
        if isinstance(value, list):
            normalized_list = []
            for item in value:
                if hasattr(item, "model_dump"):
                    normalized_list.append(item.model_dump())
                else:
                    normalized_list.append(item)
            normalized_result[key] = normalized_list
        elif hasattr(value, "model_dump"):
            normalized_result[key] = value.model_dump()
        else:
            normalized_result[key] = value

    eval_outputs = run_all_evaluators(normalized_result)

    async with AsyncSessionLocal() as session:
        for item in eval_outputs:
            await eval_repo.save_eval_record(
                session=session,
                run_id=run_id,
                evaluator_name=item["evaluator_name"],
                score=item["score"],
                passed=item["passed"],
                detail=item["detail"],
            )

def build_eval_summary(eval_rows) -> dict:
    """
    根据 eval_records 生成汇总结果。

    汇总规则：
    1. overall_eval_score = 所有 evaluator score 的平均值
    2. overall_passed = 所有 evaluator 都 passed 才为 True
    3. evaluator_count = evaluator 数量
    """
    if not eval_rows:
        return {
            "overall_eval_score": 0.0,
            "overall_passed": False,
            "evaluator_count": 0,
        }

    scores = [row.score for row in eval_rows]
    passes = [row.passed for row in eval_rows]

    overall_score = round(sum(scores) / len(scores), 4)
    overall_passed = all(passes)

    return {
        "overall_eval_score": overall_score,
        "overall_passed": overall_passed,
        "evaluator_count": len(eval_rows),
    }

def safe_parse_json(raw_text: str) -> dict:
    """
    安全解析 JSON 字符串。

    规则：
    - 能解析就返回 dict / list / 原始 JSON 对象
    - 解析失败就返回一个兜底对象，避免接口 500
    """
    if not raw_text:
        return {}

    try:
        return json.loads(raw_text)
    except Exception:
        return {
            "_raw": raw_text,
            "_parse_error": True,
        }

async def persist_approval(
    run_id: str,
    thread_id: str,
    decision: str,
    comment: str,
    stage_before: str,
    stage_after: str,
) -> None:
    """
    保存审批历史
    """
    async with AsyncSessionLocal() as session:
        await approval_repo.save_approval(
            session=session,
            run_id=run_id,
            thread_id=thread_id,
            approval_type="final_report",
            decision=decision,
            comment=comment,
            stage_before=stage_before,
            stage_after=stage_after,
        )


@router.post("/run")
async def create_research_run(request: CreateResearchRunRequest):
    """
    创建并异步执行一次研究流程。

    关键点：
    1. 为本次执行生成 thread_id
    2. 立即返回 run_id，不等待完成
    3. 后台异步执行整个流程
    4. 前端通过轮询 /research/run/{run_id} 获取进度

    返回：
    - run_id: 任务ID
    - thread_id: 线程ID
    - status: 初始状态为 'running'
    """
    try:
        thread_id = str(uuid4())

        log_event(
            event_name="research_run_start",
            payload={
                "thread_id": thread_id,
                "user_request": request.user_request,
            },
        )

        state = init_state(request.user_request, thread_id=thread_id)
        run_id = state.run_id

        config = {
            "configurable": {
                "thread_id": thread_id
            }
        }

        # 先保存初始状态
        await persist_state(thread_id, state.model_dump())

        # 后台异步执行
        async def run_workflow():
            try:
                loop = asyncio.get_event_loop()
                raw_result = await loop.run_in_executor(
                    None, lambda: app_graph.invoke(state, config=config)
                )
                # 只从 invoke 返回值中提取 interrupts 信息
                _, interrupts = normalize_graph_result(raw_result)

                # 始终从 checkpointer 读取完整状态（这是最可靠的数据源）
                checkpoint_state = await loop.run_in_executor(
                    None, lambda: app_graph.get_state(config)
                )
                if checkpoint_state and hasattr(checkpoint_state, "values"):
                    cp_values = checkpoint_state.values
                    state_dict = cp_values if isinstance(cp_values, dict) else dict(cp_values)
                else:
                    # fallback: 使用 invoke 返回值
                    state_dict, _ = normalize_graph_result(raw_result)

                state_dict["thread_id"] = thread_id

                logger.info(
                    f"run_workflow 完成: keys={list(state_dict.keys())}, "
                    f"evidence_bank={len(state_dict.get('evidence_bank', []))}, "
                    f"themes={len(state_dict.get('themes', []))}, "
                    f"insights={len(state_dict.get('insights', []))}, "
                    f"personas={len(state_dict.get('personas', []))}, "
                    f"journey_maps={len(state_dict.get('journey_maps', []))}, "
                    f"recommendations={len(state_dict.get('recommendations', []))}"
                )

                # === 诊断 dump：把 state_dict 写到文件，方便检查 ===
                try:
                    import json as _json
                    from pathlib import Path as _Path
                    def _safe_serialize(obj):
                        if hasattr(obj, 'model_dump'):
                            return obj.model_dump()
                        if isinstance(obj, list):
                            return [_safe_serialize(i) for i in obj]
                        if isinstance(obj, dict):
                            return {k: _safe_serialize(v) for k, v in obj.items()}
                        return str(obj)
                    dump_path = _Path("data") / f"debug_state_{state_dict.get('run_id', 'unknown')}.json"
                    dump_path.parent.mkdir(parents=True, exist_ok=True)
                    dump_path.write_text(_json.dumps(_safe_serialize(state_dict), ensure_ascii=False, indent=2), encoding='utf-8')
                    logger.info(f"诊断 dump 已写入: {dump_path}")
                except Exception as dump_err:
                    logger.error(f"诊断 dump 失败: {dump_err}")

                # 落库
                await persist_state(thread_id, state_dict)

                # 如果是审批中断状态，保存审批记录
                if state_dict.get("current_stage") == "review":
                    await persist_approval(
                        run_id=state_dict.get("run_id", run_id),
                        thread_id=thread_id,
                        decision="pending",
                        comment="等待审批",
                        stage_before="markdown_export",
                        stage_after="review",
                    )

                # 如果任务完成，运行评估
                if not interrupts and state_dict.get("current_stage") == "completed":
                    await persist_evals(
                        run_id=state_dict.get("run_id", run_id),
                        result=state_dict,
                    )

                log_event(
                    event_name="research_run_end",
                    payload={
                        "run_id": state_dict.get("run_id", ""),
                        "thread_id": thread_id,
                        "interrupted": bool(interrupts),
                        "current_stage": state_dict.get("current_stage", ""),
                    },
                )
            except Exception as e:
                log_event(
                    event_name="research_run_error",
                    payload={
                        "run_id": run_id,
                        "thread_id": thread_id,
                        "error": str(e),
                    },
                )

        # 启动后台任务
        import asyncio
        asyncio.create_task(run_workflow())

        return {
            "run_id": run_id,
            "thread_id": thread_id,
            "status": "running",
            "message": "任务已创建，正在执行中...",
        }

    except GuardrailError as e:
        raise HTTPException(status_code=400, detail=f"Guardrail blocked: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"POST /research/run failed: {str(e)}")

@router.post("/resume")
async def resume_research_run(request: ResumeResearchRunRequest):
    """
    恢复一条被 interrupt() 暂停的研究流程。

    关键点：
    1. 必须传同一个 thread_id
    2. 用 Command(resume=...) 恢复
    3. resume 的值会成为 interrupt() 的返回值
    """
    try:
        log_event(
            event_name="research_run_resume",
            payload={
                "thread_id": request.thread_id,
                "decision": request.decision,
            },
        )

        config = {
            "configurable": {
                "thread_id": request.thread_id
            }
        }

        # 先查恢复前状态
        loop = asyncio.get_event_loop()
        previous_state = await loop.run_in_executor(
            None, lambda: app_graph.get_state(config)
        )
        stage_before = ""
        run_id = ""
        if previous_state and getattr(previous_state, "values", None):
            values = previous_state.values
            stage_before = values.get("current_stage", "") if isinstance(values, dict) else getattr(values, "current_stage", "")
            run_id = values.get("run_id", "") if isinstance(values, dict) else getattr(values, "run_id", "")

        resume_payload = {
            "decision": request.decision,
            "comment": request.comment,
        }

        # 使用 run_in_executor 避免阻塞
        raw_result = await loop.run_in_executor(
            None, lambda: app_graph.invoke(Command(resume=resume_payload), config=config)
        )
        _, interrupts = normalize_graph_result(raw_result)

        # 始终从 checkpointer 读取完整状态
        checkpoint_state = await loop.run_in_executor(
            None, lambda: app_graph.get_state(config)
        )
        if checkpoint_state and hasattr(checkpoint_state, "values"):
            cp_values = checkpoint_state.values
            state_dict = cp_values if isinstance(cp_values, dict) else dict(cp_values)
        else:
            state_dict, _ = normalize_graph_result(raw_result)

        state_dict["thread_id"] = request.thread_id

        logger.info(
            f"resume 完成: evidence_bank={len(state_dict.get('evidence_bank', []))}, "
            f"themes={len(state_dict.get('themes', []))}, "
            f"insights={len(state_dict.get('insights', []))}"
        )

        # 用 await 直接调用（不再使用 asyncio.run）
        await persist_state(request.thread_id, state_dict)

        await persist_approval(
            run_id=state_dict.get("run_id", run_id),
            thread_id=request.thread_id,
            decision=request.decision,
            comment=request.comment,
            stage_before=stage_before,
            stage_after=state_dict.get("current_stage", ""),
        )

        await persist_evals(
            run_id=state_dict.get("run_id", run_id),
            result=state_dict,
        )

        log_event(
            event_name="research_run_resume_end",
            payload={
                "run_id": state_dict.get("run_id", ""),
                "thread_id": request.thread_id,
                "interrupted": bool(interrupts),
                "current_stage": state_dict.get("current_stage", ""),
            },
        )

        return {
            "thread_id": request.thread_id,
            "status": "interrupted" if interrupts else "completed",
            "interrupts": interrupts,
            "result": state_dict,
        }

    except GuardrailError as e:
        raise HTTPException(status_code=400, detail=f"Guardrail blocked: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"POST /research/resume failed: {str(e)}")

@router.get("/run/{run_id}")
async def get_research_run_detail(run_id: str):
    """
    查询某一次研究任务的完整详情：
    run 详情接口会返回完整 10 块：

    - run
    - evidence_items
    - themes
    - insights
    - personas
    - journey_maps
    - recommendations
    - report
    - approvals
    - traces

    """
    async with AsyncSessionLocal() as session:
        run_stmt = select(ResearchRunORM).where(ResearchRunORM.run_id == run_id)
        run_row = (await session.execute(run_stmt)).scalar_one_or_none()

        if run_row is None:
            raise HTTPException(status_code=404, detail=f"run_id 不存在: {run_id}")

        evidence_stmt = select(EvidenceORM).where(EvidenceORM.run_id == run_id)
        evidence_rows = list((await session.execute(evidence_stmt)).scalars().all())

        theme_stmt = select(ThemeORM).where(ThemeORM.run_id == run_id)
        theme_rows = list((await session.execute(theme_stmt)).scalars().all())

        insight_stmt = select(InsightORM).where(InsightORM.run_id == run_id)
        insight_rows = list((await session.execute(insight_stmt)).scalars().all())

        persona_stmt = select(PersonaORM).where(PersonaORM.run_id == run_id)
        persona_rows = list((await session.execute(persona_stmt)).scalars().all())

        journey_stmt = select(JourneyMapORM).where(JourneyMapORM.run_id == run_id)
        journey_rows = list((await session.execute(journey_stmt)).scalars().all())

        recommendation_stmt = select(RecommendationORM).where(RecommendationORM.run_id == run_id)
        recommendation_rows = list((await session.execute(recommendation_stmt)).scalars().all())

        report_stmt = select(ReportORM).where(ReportORM.run_id == run_id)
        report_row = (await session.execute(report_stmt)).scalar_one_or_none()

        approval_rows = await approval_repo.get_approvals_by_run_id(session, run_id)
        trace_rows = await trace_repo.get_traces_by_run_id(session, run_id)
       
        eval_rows = await eval_repo.get_eval_records_by_run_id(session, run_id)
        eval_summary = build_eval_summary(eval_rows)

        # 如果任务还在运行中，尝试从 checkpointer 获取最新进度
        live_stage = run_row.current_stage
        if run_row.current_stage not in ("review", "completed", "approved_or_rejected"):
            try:
                cp_config = {"configurable": {"thread_id": run_row.thread_id}}
                checkpoint_state = app_graph.get_state(cp_config)
                if checkpoint_state and hasattr(checkpoint_state, "values"):
                    cp_values = checkpoint_state.values
                    if isinstance(cp_values, dict):
                        cp_stage = cp_values.get("current_stage", "")
                    else:
                        cp_stage = getattr(cp_values, "current_stage", "")
                    if cp_stage:
                        live_stage = cp_stage
            except Exception:
                pass  # 读取失败就用数据库的值

        return {
            "run": {
                "run_id": run_row.run_id,
                "thread_id": run_row.thread_id,
                "user_request": run_row.user_request,
                "current_stage": live_stage,
                "research_goal": run_row.research_goal,
                "markdown_report_path": run_row.markdown_report_path,
            },
            "evidence_items": [
                {
                    "evidence_id": row.evidence_id,
                    "source_type": row.source_type,
                    "source_name": row.source_name,
                    "raw_excerpt": row.raw_excerpt,
                    "normalized_text": row.normalized_text,
                    "confidence": row.confidence,
                    "is_simulated": row.is_simulated,
                    "tags": row.tags.split(",") if row.tags else [],
                }
                for row in evidence_rows
            ],
            "themes": [
                {
                    "theme_id": row.theme_id,
                    "name": row.name,
                    "description": row.description,
                    "supporting_evidence_ids": row.supporting_evidence_ids.split(",") if row.supporting_evidence_ids else [],
                    "confidence_score": row.confidence_score,
                }
                for row in theme_rows
            ],
            "insights": [
                {
                    "insight_id": row.insight_id,
                    "statement": row.statement,
                    "supporting_evidence_ids": row.supporting_evidence_ids.split(",") if row.supporting_evidence_ids else [],
                    "counter_evidence_ids": row.counter_evidence_ids.split(",") if row.counter_evidence_ids else [],
                    "confidence_score": row.confidence_score,
                    "severity": row.severity,
                    "opportunity_area": row.opportunity_area,
                }
                for row in insight_rows
            ],
            "personas": [
                {
                    "persona_id": row.persona_id,
                    "name": row.name,
                    "summary": row.summary,
                    "goals": row.goals.split(",") if row.goals else [],
                    "pain_points": row.pain_points.split(",") if row.pain_points else [],
                    "behaviors": row.behaviors.split(",") if row.behaviors else [],
                    "motivations": row.motivations.split(",") if row.motivations else [],
                    "supporting_evidence_ids": row.supporting_evidence_ids.split(",") if row.supporting_evidence_ids else [],
                }
                for row in persona_rows
            ],
            "journey_maps": [
                {
                    "journey_id": row.journey_id,
                    "persona_name": row.persona_name,
                    "overview": row.overview,
                    "stages": json.loads(row.stages_json) if row.stages_json else [],
                    "supporting_evidence_ids": row.supporting_evidence_ids.split(",") if row.supporting_evidence_ids else [],
                }
                for row in journey_rows
            ],

            "recommendations": [
                {
                    "recommendation_id": row.recommendation_id,
                    "title": row.title,
                    "description": row.description,
                    "priority": row.priority,
                    "rationale": row.rationale,
                    "related_opportunity_area": row.related_opportunity_area,
                    "supporting_evidence_ids": row.supporting_evidence_ids.split(",") if row.supporting_evidence_ids else [],
                }
                for row in recommendation_rows
            ],

            "report": (
                {
                    "title": report_row.title,
                    "background": report_row.background,
                    "research_goal": report_row.research_goal,
                    "executive_summary": report_row.executive_summary,
                    "key_findings": report_row.key_findings.split("\n") if report_row.key_findings else [],
                    "themes_summary": report_row.themes_summary.split("\n") if report_row.themes_summary else [],
                    "personas_summary": report_row.personas_summary.split("\n") if report_row.personas_summary else [],
                    "journey_summary": report_row.journey_summary.split("\n") if report_row.journey_summary else [],
                    "methodology": report_row.methodology,
                    "recommendations": report_row.recommendations.split("\n") if report_row.recommendations else [],
                    "limitations": report_row.limitations.split("\n") if report_row.limitations else [],
                    "next_steps": report_row.next_steps.split("\n") if report_row.next_steps else [],
                }
                if report_row else None
            ),
            "approvals": [
                {
                    "approval_type": row.approval_type,
                    "decision": row.decision,
                    "comment": row.comment,
                    "stage_before": row.stage_before,
                    "stage_after": row.stage_after,
                }
                for row in approval_rows
            ],
            "traces": [
                {
                    "event_name": row.event_name,
                    "payload": safe_parse_json(row.payload_json),
                }
                for row in trace_rows
            ],
            "eval_summary": eval_summary,
            "eval_records": [
                {
                    "evaluator_name": row.evaluator_name,
                    "score": row.score,
                    "passed": row.passed,
                    "detail": safe_parse_json(row.detail_json),
                }
                for row in eval_rows
            ],
        }