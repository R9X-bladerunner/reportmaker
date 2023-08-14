from src.db.tables.templates import Template
from src.repositories.base import Repository


class TemplateRepository(Repository[Template]):
    model = Template
