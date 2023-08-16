from src.db.tables.patients import Patient
from src.repositories.base import Repository


class PatientRepository(Repository[Patient]):
    model = Patient
