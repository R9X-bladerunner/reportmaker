# from src.db.models.templates import Template
# from src.repositories.templates import TemplateRepository
# from src.services.base import BaseService
# from src.schemas.template import TemplateIn
#
#
# class TemplateService(BaseService[TemplateRepository, Template]):
#     repo_type = TemplateRepository
#
#     async def create_template(self, template: TemplateIn):
#         return await self.base_create(template.dict())
#
#     async def get_templates(self):
#         return await self.base_fetch_all()
#
#     async def get_template_by_id(self, template_id: int):
#         return await self.base_fetch_one(template_id)
#
#
#

