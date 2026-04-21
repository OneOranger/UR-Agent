"""
测试 LangGraph 0.2.74: 多节点 + interrupt + resume 流程中数据是否丢失。
模拟真实的12个节点的工作流。
"""
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command


class Item(BaseModel):
    id: str
    text: str

class Theme(BaseModel):
    id: str
    name: str

class TestState(BaseModel):
    run_id: str = Field(default="test-run")
    items: list[Item] = Field(default_factory=list)
    themes: list[Theme] = Field(default_factory=list)
    report: str = Field(default="")
    stage: str = Field(default="init")
    approval: str = Field(default="")


def node_ingest(state: TestState) -> TestState:
    """模拟 ingest_uploaded_files"""
    new_items = list(state.items)
    new_items.append(Item(id="ev_1", text="Evidence 1"))
    new_items.append(Item(id="ev_2", text="Evidence 2"))
    state.items = new_items
    state.stage = "theme_extractor"
    return state


def node_theme(state: TestState) -> TestState:
    """模拟 theme_extractor"""
    themes = [Theme(id="th_1", name="Theme 1"), Theme(id="th_2", name="Theme 2")]
    state.themes = themes
    state.stage = "report"
    return state


def node_report(state: TestState) -> TestState:
    """模拟 report_generator"""
    state.report = "Final Report Content"
    state.stage = "review"
    return state


def node_review(state: TestState) -> TestState:
    """模拟 request_final_approval"""
    state.stage = "waiting_approval"
    human = interrupt({"message": "请审核"})
    state.approval = human.get("decision", "") if isinstance(human, dict) else str(human)
    state.stage = "done"
    return state


# 构建图
graph = StateGraph(TestState)
graph.add_node("ingest", node_ingest)
graph.add_node("theme", node_theme)
graph.add_node("gen_report", node_report)
graph.add_node("review", node_review)
graph.set_entry_point("ingest")
graph.add_edge("ingest", "theme")
graph.add_edge("theme", "gen_report")
graph.add_edge("gen_report", "review")
graph.add_edge("review", END)

checkpointer = InMemorySaver()
app = graph.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "test-thread-full"}}
state = TestState(run_id="test-run-full")

print("=== 第一次 invoke（运行到 interrupt）===")
result1 = app.invoke(state, config=config)
print(f"返回类型: {type(result1).__name__}")
print(f"返回 keys: {list(result1.keys()) if isinstance(result1, dict) else 'N/A'}")
if isinstance(result1, dict):
    print(f"  items: {len(result1.get('items', []))}")
    print(f"  themes: {len(result1.get('themes', []))}")
    print(f"  report: '{result1.get('report', '')}'")
    print(f"  stage: '{result1.get('stage', '')}'")

print()
print("=== checkpointer 状态（interrupt 后）===")
cp1 = app.get_state(config)
v1 = cp1.values
print(f"values 类型: {type(v1).__name__}, isinstance dict: {isinstance(v1, dict)}")
if isinstance(v1, dict):
    print(f"  keys: {list(v1.keys())}")
    print(f"  items: {len(v1.get('items', []))}")
    print(f"  themes: {len(v1.get('themes', []))}")
    print(f"  report: '{v1.get('report', '')}'")
    print(f"  stage: '{v1.get('stage', '')}'")

# 模拟 normalize_graph_result
def normalize(raw):
    interrupts = []
    if isinstance(raw, dict):
        sd = dict(raw)
        ri = sd.pop("__interrupt__", None)
        if ri:
            for item in ri:
                interrupts.append({"value": getattr(item, "value", str(item))})
        return sd, interrupts
    return {"raw": str(raw)}, interrupts

state_dict1, interrupts1 = normalize(result1)
print(f"\nnormalize 后 state_dict keys: {list(state_dict1.keys())}")
print(f"  items count: {len(state_dict1.get('items', []))}")
print(f"  themes count: {len(state_dict1.get('themes', []))}")
print(f"  interrupts: {interrupts1}")

print()
print("=== Resume（恢复执行）===")
result2 = app.invoke(Command(resume={"decision": "approved"}), config=config)
print(f"返回类型: {type(result2).__name__}")
print(f"返回 keys: {list(result2.keys()) if isinstance(result2, dict) else 'N/A'}")
if isinstance(result2, dict):
    print(f"  items: {len(result2.get('items', []))}")
    print(f"  themes: {len(result2.get('themes', []))}")
    print(f"  report: '{result2.get('report', '')}'")
    print(f"  stage: '{result2.get('stage', '')}'")
    print(f"  approval: '{result2.get('approval', '')}'")

print()
print("=== checkpointer 状态（resume 后）===")
cp2 = app.get_state(config)
v2 = cp2.values
print(f"values 类型: {type(v2).__name__}, isinstance dict: {isinstance(v2, dict)}")
if isinstance(v2, dict):
    print(f"  keys: {list(v2.keys())}")
    print(f"  items: {len(v2.get('items', []))}")
    print(f"  themes: {len(v2.get('themes', []))}")
    print(f"  report: '{v2.get('report', '')}'")
    print(f"  stage: '{v2.get('stage', '')}'")
    print(f"  approval: '{v2.get('approval', '')}'")

state_dict2, interrupts2 = normalize(result2)
print(f"\nnormalize 后 state_dict keys: {list(state_dict2.keys())}")
print(f"  items count: {len(state_dict2.get('items', []))}")
print(f"  themes count: {len(state_dict2.get('themes', []))}")
