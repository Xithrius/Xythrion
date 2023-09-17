from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_main() -> None:
    response = client.get("/v1/ping")

    assert response.status_code == 200
    assert response.json() == {"ping": "some amount of time"}