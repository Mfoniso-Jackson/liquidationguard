# LiquidationGuard API Spec

Base URL in local development: `http://localhost:8000`

## `GET /health`

Returns service status.

```json
{ "status": "ok" }
```

## `POST /api/risk/calculate`

Calculates futures trade risk and stores an anonymous calculation record.

### Request

```json
{
  "account_balance": 1000,
  "direction": "Long",
  "entry_price": 100,
  "stop_price": 95,
  "leverage": 10,
  "risk_percent": 2,
  "client_metadata": { "source": "web" }
}
```

### Response

```json
{
  "calculation_id": "uuid",
  "result": {
    "position_size_units": 4,
    "notional_position_value": 400,
    "margin_required": 40,
    "money_at_risk": 20,
    "account_risk_percent": 2,
    "liquidation_price": 90,
    "distance_to_stop_percent": 5,
    "distance_to_liquidation_percent": 10,
    "liquidation_vs_stop_warning": false,
    "safety_status": "Moderate",
    "warnings": ["Liquidation estimate is approximate."],
    "interpretation": "This setup fits your chosen risk level."
  }
}
```

## `POST /api/feedback`

Stores user feedback.

### Request

```json
{
  "rating": 5,
  "message": "Useful pre-trade check.",
  "email": "trader@example.com"
}
```

### Response

```json
{
  "id": "uuid",
  "status": "received"
}
```

## `POST /api/waitlist`

Stores a Pro waitlist signup. Repeated signups with the same email return the existing record.

### Request

```json
{
  "email": "trader@example.com",
  "trader_type": "Active futures trader",
  "desired_feature": "Portfolio risk"
}
```

### Response

```json
{
  "id": "uuid",
  "status": "joined"
}
```
