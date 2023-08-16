from src.schemas.base import ApiModel


class TemplateId(ApiModel):
    id: int | None
class TemplateBase(ApiModel):
    title: str | None = None
    operator_id: int |  None = None
    html: str | None

class TemplateIn(TemplateBase):
    pass

class TemplateOut(TemplateId, TemplateBase):
    pass