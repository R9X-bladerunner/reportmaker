from fastapi import APIRouter, Depends

from src.services.templates import TemplateService

template_router = APIRouter(prefix="/templates", tags=["Template"])


@template_router.get("")
async def get_templates(service: TemplateService = Depends()):
    return await service.base_fetch_all()
