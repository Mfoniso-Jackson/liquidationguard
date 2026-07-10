# Deployment

## Local Docker Compose

From the repository root:

```bash
docker compose -f infra/docker-compose.yml up --build
```

Services:

- Web: `http://localhost:3000`
- API: `http://localhost:8000`
- PostgreSQL: `localhost:5432`

## Railway Production Deployment

Railway is the chosen production host for the current version. Deploy this monorepo as three Railway services in one project:

- `liquidationguard-db`: PostgreSQL
- `liquidationguard-api`: FastAPI backend
- `liquidationguard-web`: Next.js frontend

Railway supports monorepos by creating separate services and configuring each service's deploy settings. This repo includes Railway config files for the API and web services:

- API config: `infra/railway-api.json`
- Web config: `infra/railway-web.json`

### 1. Create Project and Database

1. Create a new Railway project.
2. Add a PostgreSQL database service.
3. Keep the database private to the Railway project.

### 2. Deploy API Service

1. Add a new service from the GitHub repo `Mfoniso-Jackson/liquidationguard`.
2. Name it `liquidationguard-api`.
3. Set the Railway config file path to:

```text
/infra/railway-api.json
```

4. Add environment variables. For `DATABASE_URL`, use Railway's reference-variable picker and select the PostgreSQL service's `DATABASE_URL`.

```bash
DATABASE_URL=${{Postgres.DATABASE_URL}}
CORS_ORIGINS=https://liquidationguard.app,https://www.liquidationguard.app
```

If you name the database service `liquidationguard-db`, Railway may display the reference as that service name instead of `Postgres`.

5. Generate a Railway domain first, then optionally add:

```text
api.liquidationguard.app
```

### 3. Deploy Web Service

1. Add another service from the same GitHub repo.
2. Name it `liquidationguard-web`.
3. Set the Railway config file path to:

```text
/infra/railway-web.json
```

4. Add the frontend environment variable after the API URL exists:

```bash
NEXT_PUBLIC_API_URL=https://api.liquidationguard.app
```

Use the temporary Railway API domain until `api.liquidationguard.app` is verified.

### 4. Custom Domains

For the web service, add:

```text
liquidationguard.app
www.liquidationguard.app
```

For the API service, add:

```text
api.liquidationguard.app
```

Railway will show the DNS records to add at your domain registrar. Add the required `CNAME` and `TXT` records, then wait for SSL verification.

### 5. Smoke Test

After deploy:

- Open `https://liquidationguard.app`
- Submit a risk calculation
- Copy the summary
- Submit feedback
- Join the Pro waitlist
- Confirm `https://api.liquidationguard.app/health` returns `{ "status": "ok" }`
