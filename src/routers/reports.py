import os

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks

from src.services.reports import ReportService

report_router = APIRouter(prefix="/reports", tags=["Reports"])

# Функция удаления временного файла отчета
def remove_file(path: str) -> None:
    os.unlink(path)

@report_router.get("/{template_id}/patients/{patient_id}")
async def get_report(
                template_id: int,
                patient_id: int,
                background_tasks: BackgroundTasks,
                service: ReportService = Depends()):

        report_file_path = await service.get_report(template_id, patient_id)
        background_tasks.add_task(remove_file, report_file_path)
        return FileResponse(report_file_path, filename='report.pdf', media_type='application/pdf')
