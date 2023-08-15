from fastapi import APIRouter, Depends

from src.schemas.template import TemplateBase, TemplateCreate, TemplateOut
from src.services.templates import TemplateService

template_router = APIRouter(prefix="/templates", tags=["Templates"])

@template_router.post("", response_model=TemplateOut)
async def add_template(
        template: TemplateCreate,
        service: TemplateService = Depends(),
        ):
    return await service.base_create(template.dict())

@template_router.get("")
async def get_templates(service: TemplateService = Depends()):
    return await service.base_fetch_all()

@template_router.get("/{template_id}", response_model=TemplateOut)
async def get_template(
        template_id: int,
        service: TemplateService = Depends()
):
    return await service.base_fetch_one(template_id)