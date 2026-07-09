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

## Production Direction

For `liquidationguard.app`, deploy:

- `apps/web` to a Next.js-capable host such as Vercel, Render, or Railway.
- `apps/api` to a Python service host such as Render, Railway, Fly.io, or a VPS.
- PostgreSQL to a managed database.

Set frontend environment:

```bash
NEXT_PUBLIC_API_URL=https://api.your-host.example
```

Set backend environment:

```bash
DATABASE_URL=postgresql+psycopg://...
CORS_ORIGINS=https://liquidationguard.app,https://www.liquidationguard.app
```

## Custom Domain

Point `liquidationguard.app` and `www.liquidationguard.app` at the frontend host. Add the exact DNS records provided by your host, then wait for SSL verification.

If the API uses a separate hostname, use something like `api.liquidationguard.app` and add it to backend CORS.
