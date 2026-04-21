from pathlib import Path

from app.tools.base.tool_result import ToolResult


def load_text_file(file_path: str) -> ToolResult:
    """
    读取本地文本文件。
    第一版只支持 txt / md。
    后面再扩展 docx / pdf / csv。
    """
    path = Path(file_path)

    if not path.exists():
        return ToolResult(success=False, error=f"文件不存在: {file_path}")

    try:
        text = path.read_text(encoding="utf-8")
        return ToolResult(
            success=True,
            data={
                "file_name": path.name,
                "content": text,
            },
        )
    except Exception as e:
        return ToolResult(success=False, error=str(e))