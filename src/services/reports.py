import os
import pdfkit
import jinja2
import tempfile

from fastapi import Depends, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import parse_obj_as


from src.schemas.patient import PatientOut
from src.services.patients import PatientService
from src.services.templates import TemplateService


# Функция удаления временного файла отчета
def remove_file(path: str) -> None:
    os.unlink(path)


class ReportService:
    def __init__(self,
                 template_service: TemplateService = Depends(),
                 patient_service: PatientService = Depends(),
                 ) -> None:

        self.template_service = template_service
        self.patient_service = patient_service


    def _parse_and_fill_template(self, html_template: str, data: dict) -> str:
        template = jinja2.Template(html_template)
        parsed_template = template.render(**data)
        return parsed_template


    async def get_report(self, template_id: int, patient_id: int, background_task: BackgroundTasks):
        # Получение данных из БД
        template = await self.template_service.get_template_by_id(template_id)
        patient = await self.patient_service.get_patient_by_id(patient_id)
        patient_as_dict = parse_obj_as(dict, PatientOut.from_orm(patient))

        # Парсинг шаблона и заполнение данными из БД
        parsed_template = self._parse_and_fill_template(template.html, patient_as_dict)

        # Создание временного пути и сохранение в PDF
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
            temp_path = temp_pdf.name
            pdfkit.from_string(parsed_template, temp_path, options={'encoding': 'utf-8'})

        #Добавление background task для удаления
        background_task.add_task(remove_file, temp_path)

        # Возврат временного пути к файлу отчету
        return FileResponse(temp_path, filename=f'{template.title}.pdf', media_type='application/pdf')




