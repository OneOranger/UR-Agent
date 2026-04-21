from pathlib import Path

from app.domain.models.evidence_item import EvidenceItem
from app.domain.models.research_state import ResearchState
from app.guardrails.engine import GuardrailEngine
from app.observability.decorators import trace_node
from app.tools.data.file_loader_tool import load_text_file


@trace_node("ingest_uploaded_files")
def ingest_uploaded_files(state: ResearchState) -> ResearchState:
    """
    从 data/raw_uploads 目录读取 txt 文件，转成正式 EvidenceItem。
    在写入 evidence_bank 之前，先经过 GuardrailEngine 检查。
    """
    raw_dir = Path("data/raw_uploads")

    if not raw_dir.exists():
        raw_dir.mkdir(parents=True, exist_ok=True)

    txt_files = list(raw_dir.glob("*.txt"))

    # 注意：必须用新列表赋值，不能用 append 原地修改
    # LangGraph StateGraph 不追踪列表的原地修改（in-place mutation）
    new_evidence = list(state.evidence_bank)

    for file_path in txt_files:
        result = load_text_file(str(file_path))
        if result.success:
            content = result.data["content"]

            evidence = EvidenceItem(
                evidence_id=f"ev_{file_path.stem}",
                source_type="file",
                source_name=file_path.name,
                raw_excerpt=content[:500],
                normalized_text=content.strip(),
                confidence=0.9,
                is_simulated=False,
                tags=["uploaded_file"],
            )

            # ===== 写入正式证据库前先做护栏检查 =====
            GuardrailEngine.validate_evidence_before_add(evidence)

            new_evidence.append(evidence)

    state.evidence_bank = new_evidence
    state.current_stage = "evidence_validator"
    return state