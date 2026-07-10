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


def test_waitlist_endpoint_is_idempotent_for_email():
    with TestClient(app) as client:
        first = client.post(
            "/api/waitlist",
            json={
                "email": "Trader@Example.com",
                "trader_type": "Active futures trader",
                "desired_feature": "Portfolio risk",
            },
        )
        second = client.post(
            "/api/waitlist",
            json={
                "email": "trader@example.com",
                "trader_type": "Scalper",
                "desired_feature": "Alerts",
            },
        )

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["id"] == second.json()["id"]
    assert first.json()["status"] == "joined"
