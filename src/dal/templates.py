from src.dal.dal import Dal
from src.db.models.tables import Template


class TemplateDal(Dal[Template]):
    model = Template

