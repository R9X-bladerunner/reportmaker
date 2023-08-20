#
# from typing import Optional
# from fastapi import APIRouter, Depends
# from src.schemas.relative import RelativeOut, RelativeIn
# from src.services.relatives import RelativeService
#
# relative_router = APIRouter(prefix="/patients/{patient_id}/relatives", tags=["Relatives"])
#
# @relative_router.get("")
# async def get_relatives(patient_id: int, service: RelativeService = Depends()):
#     return {"patient_id": patient_id}
#
# @relative_router.get("/{relative_id}")
# async def get_relative(
#         patient_id: int,
#         relative_id: int,
#         service: RelativeService = Depends()):
#     return None
#
# @relative_router.post("")
# async def create_relative(
#         patient_id: int,
#         relative: RelativeIn,
#         service: RelativeService = Depends(),
#         ):
#     pass


