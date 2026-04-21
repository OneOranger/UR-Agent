from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    全局配置类
    作用：
    1. 自动从 .env 读取配置
    2. 统一管理模型、数据库、服务端口等配置
    3. 避免把地址和 key 写死在代码里
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "UR Agent"
    APP_ENV: str = "dev"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_MODEL: str = "gpt-4.1-mini"

    LANGSMITH_TRACING: bool = False
    LANGSMITH_API_KEY: str = ""
    LANGSMITH_PROJECT: str = "ur-agent-dev"

    SQLITE_URL: str = "sqlite+aiosqlite:///./app.db"

@lru_cache
def get_settings() -> Settings:
    """
    返回单例配置对象。
    lru_cache 的作用：
    - 整个进程里只创建一次 Settings
    - 避免重复读取 .env
    """
    return Settings()