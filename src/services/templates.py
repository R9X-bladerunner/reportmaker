from src.db.tables.templates import Template
from src.repositories.templates import TemplateRepository
from src.services.base import BaseService


class TemplateService(BaseService[TemplateRepository, Template]):
    repo_type = TemplateRepository
