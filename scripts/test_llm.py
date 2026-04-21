import sys
from pathlib import Path

# 把项目根目录加入 Python 搜索路径
# __file__ 是当前文件 scripts/test_llm.py
# parents[1] 就是项目根目录 ur-agent
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from app.llm.executor import LLMExecutor
from app.domain.models.llm_outputs import ClarifiedGoalOutput



def main():
    """
    单独测试模型是否能连通。
    先不走 FastAPI，不走 LangGraph。
    只测：
    1. key 是否有效
    2. base_url 是否生效
    3. 结构化输出是否正常
    """
    executor = LLMExecutor()

    prompt = """
你是用户研究专家。
请输出结构化研究目标。

用户需求：为一个面向东京年轻白领的健身 App 做用户研究
""".strip()

    result = executor.invoke_structured(
        prompt=prompt,
        output_model=ClarifiedGoalOutput,
    )

    print(result.model_dump())


if __name__ == "__main__":
    main()