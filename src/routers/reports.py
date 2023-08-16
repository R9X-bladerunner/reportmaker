from fastapi import APIRouter, Depends


from src.services.reports import ReportService

report_router = APIRouter(prefix="/reports", tags=["Reports"])

@report_router.get("/{template_id}/patients/{patient_id}")
async def get_report(
        template_id: int,
        patient_id: int,
        service: ReportService = Depends()):
    return await service.get_report(template_id, patient_id)