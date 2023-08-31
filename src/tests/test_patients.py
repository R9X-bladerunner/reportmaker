from starlette.testclient import TestClient

from src.db.models.tables import Patient
from src.tests.data.patients import get_patient_data


async def test_patch_patient(
    client: TestClient, patient: Patient
):
    ok = client.patch(
        "/api/v1/patients/",
        params={"patient_id": patient.id},
        json=get_patient_data()
    )
    assert ok.status_code == 200, ok.text


async def test_patch_patient_405(
    client: TestClient, patient: Patient
):
    ok = client.patch(
        f"/api/v1/patients/{patient.id}",
        json=get_patient_data()
    )
    assert ok.status_code == 405, ok.text
