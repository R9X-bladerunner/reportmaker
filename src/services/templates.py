from src.db.tables.templates import Template
from src.repositories.templates import TemplateRepository
from src.services.base import BaseService
from src.schemas.template import TemplateCreate


class TemplateService(BaseService[TemplateRepository, Template]):
    repo_type = TemplateRepository


