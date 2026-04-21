from pydantic import BaseModel, Field


class ToolResult(BaseModel):
    """
    所有工具统一返回结构。
    这样做的好处：
    1. 上层节点不用关心具体工具实现
    2. 错误处理统一
    3. 后续接 tracing 更容易
    """

    success: bool = Field(..., description="工具是否成功")
    data: dict = Field(default_factory=dict, description="工具返回数据")
    error: str | None = Field(default=None, description="错误信息")