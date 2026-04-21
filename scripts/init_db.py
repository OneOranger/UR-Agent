import asyncio

from app.storage.sqlite.db import engine, Base
from app.storage.sqlite import models  # 必须导入，否则 SQLAlchemy 不知道有哪些表


async def init_db():
    """
    创建数据库表。
    第一次运行项目时执行一次即可。
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("数据库表创建完成。")


if __name__ == "__main__":
    asyncio.run(init_db())