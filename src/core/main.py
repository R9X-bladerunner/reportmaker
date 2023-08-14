from fastapi import FastAPI

from src.core.config import settings
from src.routers.templates import template_router

description = """

### Проект 

"""

app = FastAPI(
    debug=settings.debug,
    description=description,
    title=settings.app_name,
    version="0.1",
)

# -----------------------------Роуты-------------------------------------------


for r in (template_router, ):
    app.include_router(r, prefix="/api/v1"),
