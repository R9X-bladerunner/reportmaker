from src.schemas.base import ApiModel


class PatientId(ApiModel):
    id: int | None
class PatientBase(ApiModel):
    first_name: str | None
    middle_name: str |  None
    last_name: str | None
    passport_number: str | None


class PatientIn(PatientBase):
    pass

class PatientOut(PatientId, PatientBase):
    pass