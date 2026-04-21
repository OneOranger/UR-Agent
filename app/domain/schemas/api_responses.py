from pydantic import BaseModel, Field


class CreateResearchRunResponse(BaseModel):
    """
    创建研究任务后的返回结果
    """
    run_id: str = Field(..., description="任务运行ID")
    message: str = Field(..., description="返回消息")