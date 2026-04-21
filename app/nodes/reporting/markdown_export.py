from app.domain.models.research_state import ResearchState
from app.observability.decorators import trace_node
from app.tools.data.markdown_writer_tool import write_markdown_file


@trace_node("markdown_export")
def markdown_export(state: ResearchState) -> ResearchState:
    """
    把结构化 report 导出成 Markdown 文件。

    说明：
    1. 依赖 state.final_report 已经生成
    2. 导出后把 markdown 文件路径写回 state.research_plan 中，便于后续查看
    """
    if state.final_report is None:
        # 没有报告就不导出
        state.current_stage = "review"
        return state

    report = state.final_report

    markdown_lines = [
        f"# {report.title}",
        "",
        "## 一、研究背景",
        report.background or "暂无",
        "",
        "## 二、研究目标",
        report.research_goal or "暂无",
        "",
        "## 三、执行摘要",
        report.executive_summary or "暂无",
        "",
        "## 四、关键发现",
    ]

    if report.key_findings:
        for item in report.key_findings:
            markdown_lines.append(f"- {item}")
    else:
        markdown_lines.append("- 暂无")

    markdown_lines.extend([
        "",
        "## 五、主题总结",
    ])

    if report.themes_summary:
        for item in report.themes_summary:
            markdown_lines.append(f"- {item}")
    else:
        markdown_lines.append("- 暂无")

    markdown_lines.extend([
        "",
        "## 六、用户画像总结",
    ])

    if report.personas_summary:
        for item in report.personas_summary:
            markdown_lines.append(f"- {item}")
    else:
        markdown_lines.append("- 暂无")

    markdown_lines.extend([
        "",
        "## 七、用户旅程总结",
    ])

    if report.journey_summary:
        for item in report.journey_summary:
            markdown_lines.append(f"- {item}")
    else:
        markdown_lines.append("- 暂无")

    markdown_lines.extend([
        "",
        "## 八、关键洞察",
    ])

    if report.insights:
        for insight in report.insights:
            markdown_lines.append(f"- {insight.statement}")
    else:
        markdown_lines.append("- 暂无")

    markdown_lines.extend([
        "",
        "## 九、建议",
    ])

    if report.recommendations:
        for item in report.recommendations:
            markdown_lines.append(f"- {item}")
    else:
        markdown_lines.append("- 暂无")

    markdown_lines.extend([
        "",
        "## 十、研究方法",
        report.methodology or "暂无",
        "",
        "## 十一、局限性",
    ])

    if report.limitations:
        for item in report.limitations:
            markdown_lines.append(f"- {item}")
    else:
        markdown_lines.append("- 暂无")

    markdown_lines.extend([
        "",
        "## 十二、下一步",
    ])

    if report.next_steps:
        for item in report.next_steps:
            markdown_lines.append(f"- {item}")
    else:
        markdown_lines.append("- 暂无")

    markdown_content = "\n".join(markdown_lines)

    output_path = f"data/reports/{state.run_id}.md"
    saved_path = write_markdown_file(output_path, markdown_content)

    # 把导出路径放回 research_plan，第一版先这样存
    state.research_plan["markdown_report_path"] = saved_path

    # 导出后继续进入 review
    state.current_stage = "review"
    return state