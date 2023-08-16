
from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.responses import FileResponse


from src.services.reports import ReportService

report_router = APIRouter(prefix="/reports", tags=["Reports"])



@report_router.get("/{template_id}/patients/{patient_id}")
async def get_report(
                template_id: int,
                patient_id: int,
                background_tasks: BackgroundTasks,
                service: ReportService = Depends()) -> FileResponse:

        report_file_responce = await service.get_report(template_id, patient_id, background_tasks)
        return report_file_responce
