# from ..db.models.tables import Patient
# from ..schemas.patient import PatientIn, PatientUpdate
# from ..schemas.relative import RelativeUpdate, RelativeIn
# from ..utils.errors import RecordAlreadyExistError
# from sqlalchemy import delete, insert, select, update
# from collections.abc import Mapping
# from  dal import Dal
#
# class RelativeDal(Dal[Patient]):
#     model = Patient
#
#     def update_by_id(self, relative_id: int, data: RelativeUpdate) -> Patient | None:
#         relative =
#         filters = {'id': relative_id}
#         patch = data.dict(exclude_unset=True)
#         return self.update(filters, patch)
#
#     def create(self, schema: RelativeIn) -> Patient:
#         relative = Patient(**schema.dict(), is_patient=False)
#         return self.add_orm(relative)
#
#     def get_by_id(self, relative_id: int) -> Patient | None:
#         relative = self.get_(relative_id)
#         if relative:
#             if relative.is_patient
#         return self.get_(patient_id)
#     #
#     def get_all_or_limit (self, limit: int = None) -> list[Patient] | None:
#
#         stmt = select(self.model).where(self.model.is_patient == True)
#         return self.fetch_all()
#
#
#     def delete_patient(self):
#         pass
