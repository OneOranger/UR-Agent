from typing import Type

from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from app.core.config import get_settings
from app.observability.tracing import log_event, now_ms


class LLMExecutor:
    """
    统一的大模型调用器。

    作用：
    1. 统一创建模型客户端
    2. 支持结构化输出
    3. 支持从 .env 读取代理地址 base_url
    """

    def __init__(self):
        settings = get_settings()

        print("DEBUG OPENAI_MODEL =", settings.OPENAI_MODEL)
        print("DEBUG OPENAI_BASE_URL =", settings.OPENAI_BASE_URL)
        print("DEBUG API KEY EXISTS =", bool(settings.OPENAI_API_KEY))

        self.model_name = settings.OPENAI_MODEL
        self.base_url = settings.OPENAI_BASE_URL

        self.model = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL,   # 关键：把代理地址传进去
            temperature=0,
        )

    
    def invoke_structured(self, prompt: str, output_model: Type[BaseModel]) -> BaseModel:
        """
        调用模型，并返回结构化输出。

        参数：
        - prompt: 提示词
        - output_model: Pydantic 输出模型

        返回：
        - output_model 对应实例
        """
        start_time = now_ms()

        log_event(
            event_name="llm_call_start",
            payload={
                "model": self.model_name,
                "base_url": self.base_url,
                "output_model": output_model.__name__,
                "prompt_preview": prompt[:400],  # 只打前200字符，避免日志过长
            },
        )

        structured_llm = self.model.with_structured_output(output_model)
        result = structured_llm.invoke(prompt)

        duration_ms = round(now_ms() - start_time, 2)

        log_event(
            event_name="llm_call_end",
            payload={
                "model": self.model_name,
                "output_model": output_model.__name__,
                "duration_ms": duration_ms,
                "result_preview": str(result)[:200],
            },
        )

        return result