import os

from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.responses import FileResponse


from src.services.services import ReportService

report_router = APIRouter(prefix="/reports", tags=["Reports"])



@report_router.get("/reports/patients/{patient_id}")
def get_patient_report(patient_id: int,
                background_task: BackgroundTasks,
                service: ReportService = Depends()) -> FileResponse:


    report_file_path, report_file_name = service.get_patient_report(patient_id)
    background_task.add_task(os.remove, report_file_path)

    return FileResponse(report_file_path,
                        filename=report_file_name,
                        media_type='application/pdf',
                        background=background_task)
