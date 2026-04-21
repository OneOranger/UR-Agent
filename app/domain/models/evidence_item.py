from typing import Literal
from pydantic import BaseModel, Field


class EvidenceItem(BaseModel):
    """
    证据项：用户研究系统的灵魂对象。
    任何洞察都必须能回溯到一个或多个 EvidenceItem。
    """

    evidence_id: str = Field(..., description="证据唯一ID")
    source_type: Literal["file", "web", "survey", "interview", "simulated"] = Field(
        ...,
        description="证据来源类型。simulated 只能用于演练，不能作为正式结论依据。",
    )
    source_name: str = Field(..., description="来源名称，如文件名、网页标题")
    raw_excerpt: str = Field(..., description="原始摘录，尽量保留证据原文")
    normalized_text: str = Field(..., description="清洗后的文本，便于后续分析")
    confidence: float = Field(ge=0.0, le=1.0, description="证据可信度分数")
    is_simulated: bool = Field(default=False, description="是否是模拟数据")
    tags: list[str] = Field(default_factory=list, description="证据标签")