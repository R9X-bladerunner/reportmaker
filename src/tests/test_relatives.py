from starlette.testclient import TestClient

from src.db.models.tables import Relative
from src.tests.data.documents import get_document_data
from src.tests.data.relatives import get_relative_data


async def test_get_relatives(
    client: TestClient, relative: Relative
):
    ok = client.get("/api/v1/relatives/")
    assert ok.status_code == 200, ok.text


async def test_get_relative(
    client: TestClient, relative: Relative
):
    ok = client.get(
        f"/api/v1/relatives/{relative.id}")
    assert ok.status_code == 200, ok.text


async def test_delete_relative(
    client: TestClient, relative: Relative
):
    ok = client.delete(f"/api/v1/relatives/{relative.id}")
    assert ok.status_code == 204, ok.text


async def test_patch_relative(
    client: TestClient, relative: Relative
):
    ok = client.patch(
        f"/api/v1/relatives/{relative.id}",
        json=get_relative_data(withreltype=False)
    )
    assert ok.status_code == 200, ok.text


async def test_get_relative_patients(
    client: TestClient, relative: Relative
):
    ok = client.get(
        f"/api/v1/relatives/{relative.id}/patients")
    assert ok.status_code == 200, ok.text


async def test_get_relative_documents(
    client: TestClient, relative: Relative
):
    ok = client.get(
        f"/api/v1/relatives/{relative.id}/documents")
    assert ok.status_code == 200, ok.text

async def test_create_relative_document(
    client: TestClient, relative: Relative
):
    ok = client.post(f"/api/v1/relatives/{relative.id}/documents",
                     json=get_document_data())
    assert ok.status_code == 201, ok.text




