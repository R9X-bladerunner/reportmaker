from fastapi import Depends

from src.schemas.patient import PatientOut
from src.services.patients import PatientService
from src.services.templates import TemplateService


from jinja2 import Template

class HtmlParser:

    def parse_and_fill_template(self, html_template: str, data: dict) -> str:
        template = Template(html_template)
        parsed_template = template.render(**data)
        return parsed_template



class ReportService:
    def __init__(self,
                 template_service: TemplateService = Depends(),
                 patient_service: PatientService = Depends(),
                 html_parser: HtmlParser = Depends(),
                 ) -> None:

        self.template_service = template_service
        self.patient_service = patient_service
        self.html_parser = html_parser

    async def get_template(self, temlp_id: int):
        return await self.template_service.base_fetch_one(temlp_id)

    async def get_report(self, template_id: int, patient_id: int):
        template = await self.template_service.get_template_by_id(template_id)
        patient = await self.patient_service.get_patient_by_id(patient_id)
        patient_dict = PatientOut.from_orm(patient).dict()

        return self.html_parser.parse_and_fill_template(template.html, patient_dict)
