# LiquidationGuard.app

LiquidationGuard.app is a production-grade pre-trade risk decision tool for futures traders.

Core promise: **Know your risk before you enter a trade.**

It helps traders estimate position size, notional value, margin requirement, money at risk, account risk, approximate liquidation price, liquidation distance, warnings, and a plain-English trade risk interpretation.

## Stack

- Next.js + TypeScript frontend
- Tailwind CSS
- FastAPI backend
- PostgreSQL persistence
- SQLAlchemy ORM
- Pydantic validation
- Docker Compose for local development
- pytest backend tests
- Playwright frontend E2E test

## Repository Structure

```text
apps/
  web/      Next.js app
  api/      FastAPI app
packages/
  shared/   Shared schema/type home for future growth
infra/
  docker-compose.yml
docs/
  product-spec.md
  api-spec.md
  deployment.md
```

## Local Development with Docker

```bash
docker compose -f infra/docker-compose.yml up --build
```

Open:

- Web: `http://localhost:3000`
- API health: `http://localhost:8000/health`

## Backend Development

```bash
cd apps/api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Run backend tests:

```bash
cd apps/api
pytest
```

## Frontend Development

```bash
cd apps/web
npm install
npm run dev
```

Run frontend E2E:

```bash
cd apps/web
npm run test:e2e
```

## Environment Files

Copy examples before local non-Docker development:

```bash
cp apps/api/.env.example apps/api/.env
cp apps/web/.env.example apps/web/.env.local
```

## Disclaimer

This is an educational risk estimation tool, not financial advice. Exchange-specific liquidation prices may differ due to fees, maintenance margin, funding, margin mode, and exchange rules.
