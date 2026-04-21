
from fastapi import FastAPI

from app.api.routes.research_runs import router as research_router
from app.core.config import get_settings
from app.core.logger import setup_logger

settings = get_settings()
logger = setup_logger()

app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
)


@app.get("/")
def root():
    """
    根路径首页。
    浏览器访问 http://127.0.0.1:8002/ 时会看到这里的返回内容。
    """
    return {
        "message": "UR Agent 服务已启动",
        "docs_url": "/docs",
        "health_url": "/health"
    }


@app.get("/health")
def health():
    """
    健康检查接口。
    用于确认服务是否正常启动。
    """
    return {
        "status": "ok",
        "app_name": settings.APP_NAME,
        "env": settings.APP_ENV,
    }


app.include_router(research_router)

logger.info("UR Agent application initialized.")