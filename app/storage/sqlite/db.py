from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from app.core.config import get_settings

settings = get_settings()

# 创建异步数据库引擎
# 这里会读取 .env 里的 SQLITE_URL
engine = create_async_engine(
    settings.SQLITE_URL,
    echo=False,  # True 时会打印 SQL，调试时可打开
)

# 创建异步 Session 工厂
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# 所有 ORM 表模型都继承这个 Base
Base = declarative_base()


async def get_db_session() -> AsyncSession:
    """
    获取数据库会话。
    后面 FastAPI 也可以把它做成依赖注入。
    """
    async with AsyncSessionLocal() as session:
        yield session