from pathlib import Path


def write_markdown_file(file_path: str, content: str) -> str:
    """
    把 Markdown 内容写入本地文件，并返回最终文件路径。

    参数：
    - file_path: 目标文件路径
    - content: Markdown 文本内容

    返回：
    - 实际写入的文件路径字符串
    """
    path = Path(file_path)

    # 如果父目录不存在，就自动创建
    path.parent.mkdir(parents=True, exist_ok=True)

    # 以 utf-8 编码写入，避免中文乱码
    path.write_text(content, encoding="utf-8")

    return str(path)