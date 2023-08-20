from typing import Optional, List

from fastapi import Depends
from sqlalchemy.orm import Session, query
from src.db.connection import get_session
from src.db.models.tables import Patient
from sqlalchemy import  delete, insert, update


class PatientRepository:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
        self.model = Patient

        print('patient_repo_init')

    def get_by_id(self, patient_id: int) -> Optional[Patient]:
        return self.session.query(Patient).filter(self.model.id == patient_id).first()

    def get_all(self) -> list[type(Patient)]:
        return self.session.query(Patient).all()

    def create(self, patient: Patient) -> Patient:
        self.session.add(patient)
        self.session.commit()
        return patient

    def update(self, patient: Patient) -> Patient:
        self.session.commit()
        return patient

    def delete_by_id(self, patient_id: int) -> None:
        stmt = delete(self.model).where(self.model.id == patient_id)
        self.session.execute(stmt)
        self.session.commit()



