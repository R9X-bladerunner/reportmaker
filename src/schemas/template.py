from src.schemas.base import ApiModel
from fastapi import Path

class TemplateId(ApiModel):
    id: int | None
class TemplateBase(ApiModel):
    title: str | None = None
    operator_id: int |  None = None
    html: str | None

class TemplateCreate(TemplateBase):
    pass

class TemplateOut(TemplateId, TemplateBase):
    pass