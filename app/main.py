import logging

import uvicorn

from api import router as api_router
from core.config import settings
from create_app import create

logging.basicConfig(
    format=settings.logging.log_format,
    level=settings.logging.log_level_value,
)

main_app = create()
main_app.include_router(
    api_router,
)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
