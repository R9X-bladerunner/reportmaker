from starlette.testclient import TestClient

from src.db.models.tables import Patient
from src.tests.data.documents import get_document_data
from src.tests.data.patients import get_patient_data
from src.tests.data.relatives import get_relative_data


async def test_get_patients(
    client: TestClient, patient: Patient
):
    ok = client.get("/api/v1/patients/")
    assert ok.status_code == 200, ok.text


async def test_create_patient(
    client: TestClient
):
    patient_data = get_patient_data()
    ok = client.post("/api/v1/patients/",
                     json=patient_data)
    assert ok.status_code == 201, ok.text


async def test_get_patient(
    client: TestClient, patient: Patient
):
    ok = client.get(
        f"/api/v1/patients/{patient.id}")
    assert ok.status_code == 200, ok.text


async def test_delete_patient(
    client: TestClient, patient: Patient
):
    ok = client.get("/api/v1/patients/")
    assert ok.status_code == 200, ok.text


async def test_patch_patient(
    client: TestClient, patient: Patient
):
    ok = client.patch(
        f"/api/v1/patients/{patient.id}",
        json=get_patient_data()
    )
    assert ok.status_code == 200, ok.text


async def test_patch_patient_405(
    client: TestClient, patient: Patient
):
    ok = client.patch(
        "/api/v1/patients/",
        params={"patient_id": patient.id},
        json=get_patient_data()
    )
    assert ok.status_code == 405, ok.text

async def test_get_relatives(
    client: TestClient, patient: Patient
):
    ok = client.get(f"/api/v1/patients/{patient.id}/relatives")

    assert ok.status_code == 200, ok.text

async def test_create_relative(
    client: TestClient, patient: Patient
):
    ok = client.post(f"/api/v1/patients/{patient.id}/relatives",
                     json=get_relative_data())

    assert ok.status_code == 201, ok.text

async def test_get_patient_documents(
    client: TestClient, patient: Patient
):
    ok = client.get(f"/api/v1/patients/{patient.id}/documents")


    assert ok.status_code == 200, ok.text

async def test_create_patient_document(
        client: TestClient, patient: Patient
):
    ok = client.post(f"/api/v1/patients/{patient.id}/documents",
                     json=get_document_data())
    assert ok.status_code == 201, ok.text


