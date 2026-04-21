from pydantic import BaseModel, Field


class CreateResearchRunRequest(BaseModel):
    """
    创建研究任务的请求体
    """
    user_request: str = Field(..., description="用户输入的研究需求")