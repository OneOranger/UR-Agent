from pydantic import BaseModel, Field
from typing import Literal


class ResumeResearchRunRequest(BaseModel):
    """
    恢复研究流程的请求体。

    thread_id:
    - 这次图执行对应的线程ID
    - LangGraph 用它找到之前保存的状态

    decision:
    - 人工审批结果
    - approved 表示通过
    - rejected 表示驳回
    """

    thread_id: str = Field(..., description="LangGraph 线程ID")
    decision: Literal["approved", "rejected"] = Field(..., description="审批结果")
    comment: str = Field(default="", description="审批备注")