from langgraph.checkpoint.memory import InMemorySaver


def get_checkpointer():
    """
    返回 LangGraph 的内存版 checkpointer。

    说明：
    1. 这个版本适合本地开发和调试
    2. 它可以在 interrupt() 发生时保存状态
    3. 生产环境不要用它，生产环境要换成持久化存储

    LangGraph 官方文档说明：
    - interrupt 需要 checkpointer 才能暂停并恢复
    - checkpointer 会按 thread_id 保存状态
    """
    return InMemorySaver()