# from fastapi import APIRouter, Depends, Path
#
# from src.schemas.template import TemplateIn, TemplateOut
# # from src.services.templates import TemplateService
#
# template_router = APIRouter(prefix="/templates", tags=["Templates"])
#
# @template_router.get("", response_model=list[TemplateOut])
# async def get_templates(service: TemplateService = Depends()):
#     return await service.get_templates()
#
# @template_router.get("/{template_id}", response_model=TemplateOut)
# async def get_template(
#         template_id: int = Path(gt=0),
#         service: TemplateService = Depends()
# ):
#     return await service.get_template_by_id(template_id)
#
# @template_router.post("", response_model=TemplateOut)
# async def create_template(
#         template: TemplateIn,
#         service: TemplateService = Depends(),
#         ):
#     return await service.create_template(template)
#
