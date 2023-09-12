from starlette.testclient import TestClient

from src.db.models.tables import Document
from src.tests.data.documents import get_document_data


async def test_get_documents(
    client: TestClient, document: Document
):
    ok = client.get("/api/v1/documents/")
    assert ok.status_code == 200, ok.text

async def test_get_document(
    client: TestClient, document: Document
):
    ok = client.get(
        f"/api/v1/documents/{document.id}")
    assert ok.status_code == 200, ok.text

async def test_delete_document(
    client: TestClient, document: Document
):
    ok = client.delete(f"/api/v1/documents/{document.id}")
    assert ok.status_code == 200, ok.text


async def test_patch_document(
    client: TestClient, document: Document
):
    ok = client.patch(
        f"/api/v1/documents/{document.id}",
        json=get_document_data()
    )
    assert ok.status_code == 200, ok.text


async def test_get_owner(
    client: TestClient, document: Document
):
    ok = client.get(
        f"/api/v1/documents/{document.id}/owner")
    assert ok.status_code == 200, ok.text