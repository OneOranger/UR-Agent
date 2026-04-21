"""
测试 LangGraph 0.2.74 + Pydantic StateGraph 对 list 字段的处理行为。
不需要 LLM 调用。
"""
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import InMemorySaver


class Item(BaseModel):
    id: str
    text: str


class TestState(BaseModel):
    run_id: str = Field(default="test-run")
    items: list[Item] = Field(default_factory=list)
    name: str = Field(default="")
    stage: str = Field(default="init")


def node_a(state: TestState) -> TestState:
    """模拟 ingest_uploaded_files：用新列表赋值"""
    new_items = list(state.items)
    new_items.append(Item(id="item_1", text="Hello"))
    new_items.append(Item(id="item_2", text="World"))
    state.items = new_items
    state.stage = "node_b"
    return state


def node_b(state: TestState) -> TestState:
    """模拟 theme_extractor：直接赋值新列表"""
    state.name = "Test Name"
    state.stage = "end"
    return state


# 构建图
graph = StateGraph(TestState)
graph.add_node("node_a", node_a)
graph.add_node("node_b", node_b)
graph.set_entry_point("node_a")
graph.add_edge("node_a", "node_b")
graph.add_edge("node_b", END)

checkpointer = InMemorySaver()
app = graph.compile(checkpointer=checkpointer)

# 运行
config = {"configurable": {"thread_id": "test-thread-1"}}
state = TestState(run_id="test-run-1")

print("=== 测试1: 正常运行（无 interrupt）===")
result = app.invoke(state, config=config)
print(f"invoke 返回类型: {type(result).__name__}")
print(f"invoke 返回值: {result}")
print(f"isinstance(result, dict): {isinstance(result, dict)}")

if isinstance(result, dict):
    print(f"  keys: {list(result.keys())}")
    print(f"  items: {result.get('items')}")
    print(f"  items count: {len(result.get('items', []))}")
    print(f"  name: {result.get('name')}")
else:
    print(f"  dir: {[x for x in dir(result) if not x.startswith('_')]}")

print()

# 检查 checkpointer
cp_state = app.get_state(config)
print(f"checkpointer values 类型: {type(cp_state.values).__name__}")
cp_values = cp_state.values
print(f"isinstance(cp_values, dict): {isinstance(cp_values, dict)}")

if isinstance(cp_values, dict):
    print(f"  keys: {list(cp_values.keys())}")
    print(f"  items: {cp_values.get('items')}")
    print(f"  items count: {len(cp_values.get('items', []))}")
    for item in cp_values.get('items', []):
        print(f"    item type: {type(item).__name__}, value: {item}")
else:
    cp_dict = dict(cp_values)
    print(f"  dict(cp_values) keys: {list(cp_dict.keys())}")
    print(f"  items: {cp_dict.get('items')}")

print()
print("=== 测试2: 带 interrupt 的运行 ===")
from langgraph.types import interrupt

def node_c(state: TestState) -> TestState:
    """模拟 ingest：添加数据"""
    new_items = list(state.items)
    new_items.append(Item(id="item_3", text="Interrupted"))
    state.items = new_items
    state.stage = "node_d"
    return state

def node_d(state: TestState) -> TestState:
    """模拟 request_final_approval：interrupt"""
    state.stage = "waiting"
    human = interrupt({"message": "please approve"})
    state.name = f"approved: {human}"
    state.stage = "done"
    return state

graph2 = StateGraph(TestState)
graph2.add_node("node_c", node_c)
graph2.add_node("node_d", node_d)
graph2.set_entry_point("node_c")
graph2.add_edge("node_c", "node_d")
graph2.add_edge("node_d", END)

checkpointer2 = InMemorySaver()
app2 = graph2.compile(checkpointer=checkpointer2)

config2 = {"configurable": {"thread_id": "test-thread-2"}}
state2 = TestState(run_id="test-run-2")

result2 = app2.invoke(state2, config=config2)
print(f"interrupt invoke 返回类型: {type(result2).__name__}")
print(f"interrupt invoke 返回值: {result2}")
if isinstance(result2, dict):
    print(f"  keys: {list(result2.keys())}")
    print(f"  items: {result2.get('items')}")
    print(f"  items count: {len(result2.get('items', []))}")
    has_interrupt = '__interrupt__' in result2
    print(f"  has __interrupt__: {has_interrupt}")
print()

# 检查 checkpointer
cp_state2 = app2.get_state(config2)
print(f"interrupt checkpointer values 类型: {type(cp_state2.values).__name__}")
cp_values2 = cp_state2.values
if isinstance(cp_values2, dict):
    print(f"  keys: {list(cp_values2.keys())}")
    print(f"  items count: {len(cp_values2.get('items', []))}")
    for item in cp_values2.get('items', []):
        print(f"    item type: {type(item).__name__}, value: {item}")
    print(f"  stage: {cp_values2.get('stage')}")
else:
    print(f"  type: {type(cp_values2)}")
    cp_dict2 = dict(cp_values2)
    print(f"  dict keys: {list(cp_dict2.keys())}")
    print(f"  items count: {len(cp_dict2.get('items', []))}")
