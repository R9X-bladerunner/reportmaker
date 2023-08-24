from fastapi import FastAPI

from src.core.config import settings
from src.routers.patients import patient_router
from src.routers.relatives import relative_router

# from src.routers.reports import report_router
# from src.routers.templates import template_router

description = """

###  Сервис для генерации pdf отчетов по html-шаблонам

"""

app = FastAPI(
    debug=settings.debug,
    description=description,
    title=settings.app_name,
    version="0.1",
)

# -----------------------------Роуты-------------------------------------------


for r in (patient_router, relative_router):
    app.include_router(r, prefix="/api/v1"),
