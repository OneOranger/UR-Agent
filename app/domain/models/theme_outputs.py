from pydantic import BaseModel, Field


class ThemeDraftOutput(BaseModel):
    """
    单条主题草稿
    """
    name: str = Field(..., description="主题名称")
    description: str = Field(..., description="主题说明")
    confidence_score: float = Field(
        ge=0.0,
        le=1.0,
        default=0.8,
        description="主题置信度",
    )


class ThemeListOutput(BaseModel):
    """
    多条主题输出
    """
    themes: list[ThemeDraftOutput] = Field(default_factory=list, description="主题列表")