from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint():
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_calculate_endpoint_persists_and_returns_result():
    with TestClient(app) as client:
        response = client.post(
            "/api/risk/calculate",
            json={
                "account_balance": 1000,
                "direction": "Long",
                "entry_price": 100,
                "stop_price": 95,
                "leverage": 10,
                "risk_percent": 2,
            },
        )

    assert response.status_code == 200
    body = response.json()
    assert body["calculation_id"]
    assert body["result"]["position_size_units"] == 4
    assert body["result"]["safety_status"] == "Moderate"
