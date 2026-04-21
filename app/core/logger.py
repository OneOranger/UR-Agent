import logging


def setup_logger() -> logging.Logger:
    """
    创建全局日志对象。
    第一版先用最简单的 logging。
    后面你可以替换成 structlog / loguru / OpenTelemetry。
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    return logging.getLogger("ur_agent")