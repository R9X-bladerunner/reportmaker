
import tempfile

import jinja2
import pdfkit
from fastapi import Depends, status
from sqlalchemy.orm import joinedload

from src.dal.documents import DocumentDal
from src.dal.patients import PatientDal
from src.dal.relatives import RelativeDal
from src.db.models.tables import Patient, Relative, Document, Relationship
from src.schemas.document import DocumentIn, DocumentUpdate
from src.schemas.patient import PatientIn, PatientUpdate, PatientOutWithRelType
from src.schemas.relative import RelativeIn, RelativeOut, RelativeUpdate


class PatientService:
    def __init__(self, patient_dal: PatientDal = Depends()):
        self.dal = patient_dal

    def get_patients(self):
        return self.dal.get_patients()

    def get_patient_by_id(self, patient_id: int):
        return self.dal.get_patient_by_id(patient_id)

    def create_patient(self, patient: PatientIn):
        return self.dal.create(patient)

    def update_patient_by_id(self, patient_id: int, data: PatientUpdate) -> Patient | None:
        return self.dal.update_patient_by_id(patient_id, data)

    def delete_patient(self, patient_id: int) -> None:
        return self.dal.delete_by_id(patient_id)

    def create_relative(self, patient_id: int,
                        relative_data: RelativeIn) -> RelativeOut:

        relative, relation = self.dal.create_relative(patient_id, relative_data)
        return RelativeOut(
            relationship_type = relation.relationship_type,
            **vars(relative))

    def get_patient_relatives(self, patient_id: int) -> list[RelativeOut]:
        patient = self.dal.get_patient_w_relationship_a_relative(patient_id)

        return [RelativeOut(
            relationship_type = ra.relationship_type,
            **vars(ra.relative)
        ) for ra in patient.relative_association]


    def create_document(self, patient_id: int,
                        document_data: DocumentIn):
        return self.dal.create_document(patient_id, document_data)

    def get_patient_documents(self, patient_id: int) -> list[Document]:
        documents = self.dal.get_patient_documents(patient_id)
        return documents


class RelativeService:
    def __init__(self, relative_dal: RelativeDal = Depends()):
        self.dal = relative_dal

    def get_relatives(self) -> list[Relative]:
        return self.dal.get_relatives()

    def get_relative_by_id(self, relative_id: int) -> Relative:
        return self.dal.get_relative_by_id(relative_id)


    def get_relative_patients(self, relative_id: int) -> list[PatientOutWithRelType]:
        relative = self.dal.get_relative_w_relationship_a_patient(relative_id)
        return [PatientOutWithRelType(
            relative_to_patient_as=ra.relationship_type,
            **vars(ra.patient)
        ) for ra in relative.relative_association]

    def create_document(self, relative_id: int,
                        document_data: DocumentIn):
        return self.dal.create_document(relative_id, document_data)

    def get_relative_documents(self, relative_id: int) -> list[Document]:
        documents = self.dal.get_relative_documents(relative_id)
        return documents

    def update_relative_by_id(self, relative_id: int, data: RelativeUpdate) -> Relative:
        return self.dal.update_relative_by_id(relative_id, data)

    def delete_relative_by_id(self, relative_id: int) -> status.HTTP_204_NO_CONTENT:
        self.dal.delete_by_id(relative_id)
        return None


class DocumentService:
    def __init__(self, document_dal: DocumentDal = Depends()):
        self.dal = document_dal

    def get_documents(self) -> list[Document]:
        return self.dal.get_documents()

    def get_document_by_id(self, document_id: int) -> Document:
        return self.dal.get_document_by_id(document_id)

    def update_document_by_id(self, document_id: int, data: DocumentUpdate) -> Document | None:
        return self.dal.update_document_by_id(document_id, data)

    def delete_document(self, document_id: int) -> None:
        return self.dal.delete_document(document_id)
    def get_owner(self, document_id: int):
        return self.dal.get_owner(document_id)

class ReportService:
    def __init__(self, patient_service: PatientService = Depends()):
        self.patient_service = patient_service


    @staticmethod
    def _parse_and_fill_template(template_file_name: str, data: dict) -> str:
        template_loader = jinja2.FileSystemLoader(searchpath="/reportmaker/src/basic_templates")
        template_env = jinja2.Environment(loader=template_loader)
        template_file = template_file_name
        template = template_env.get_template(template_file)
        parsed_template = template.render(**data)
        return parsed_template

    def fill_report(self, template_file_name: str, list_data: list[dict]) -> str:
        parsed_report = ''
        for item in list_data:
            parsed_item = self._parse_and_fill_template(template_file_name, item)
            parsed_report = f'{parsed_report}{parsed_item}\n'

        return parsed_report

    @staticmethod
    def make_report_file_path(parsed_report: str) -> str:
        # Создание временного пути и сохранение в PDF
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
            temp_path = temp_pdf.name
            pdfkit.from_string(parsed_report, temp_path, options={'encoding': 'utf-8'})

        print(f'tempfilepath:     {temp_path}')  # отладка

        return temp_path

    def get_patient_report(self, patient_id: int) -> (str, str):

        patient = self.patient_service.dal.get_patient_by_id(patient_id,
            options=[joinedload(Patient.relative_association).joinedload(
                Relationship.relative).joinedload(Relative.documents)])

        # extracting from models to list[dict]
        patient_dict = {**vars(patient)}

        patient_docs = [{**vars(document),
                                   'last_name': patient.last_name,
                                   'first_name': patient.first_name,
                                   'middle_name': patient.middle_name} for document in patient.documents]

        patient_report = self.fill_report('patient_info.html', [patient_dict])
        patient_docs_report = self.fill_report("document_info.html", patient_docs)

        rel_w_doc_report = ''
        for relation in patient.relative_association:
            rel_w_doc_report = rel_w_doc_report + self.fill_report(
                'relative_info.html',
                [{**vars(relation.relative),
                    'relationship_type': relation.relationship_type}]
                ) + '\n'
            for document in relation.relative.documents:
                rel_w_doc_report = rel_w_doc_report + self.fill_report(
                    'document_info.html',
                    [{**vars(document),
                      'last_name': relation.relative.last_name,
                      'first_name': relation.relative.first_name,
                      'middle_name': relation.relative.middle_name
                      }]
                    ) + '\n'


        common_report = f'{patient_report}{patient_docs_report}{rel_w_doc_report}'
        report_file_path = self.make_report_file_path(common_report)
        report_file_name = f'report_for_patient_id_{patient.id}'

        return report_file_path, report_file_name




