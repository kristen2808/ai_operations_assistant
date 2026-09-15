# AI Operations Assistant

Backend API pro AI Operations Assistant aplikaci.

## Struktura projektu

```
ai_operations_assistant/
├── backend/
│   ├── main.py              # Entry point aplikace
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI app s routes a deps
│   │   ├── config.py        # Environment config
│   │   ├── database.py      # SQLAlchemy async engine
│   │   └── schemas.py       # Pydantic schemas
│   │   └── routers/         # API routes
│   │       ├── __init__.py
│   │       └── health.py    # /health endpoint
│   └── alembic/             # Database migrations (nevytvoreno)
├── docker/
│   ├── postgres/
│   │   └── init.sql         # Database schema (stávající)
│   └── backend/
│       └── Dockerfile       # Backend Docker image
├── docker-compose.yaml      # Docker orchestrace
├── pyproject.toml          # Dependencies (uv)
└── README.md               # Tento soubor
```

## Instalace a spouštění

### 1. Spusť PostgreSQL

```bash
docker-compose up -d postgres
```

Počkej cca 30 sekund pro inicializaci databáze.

### 2. (Volitelné) Spusť backend

```bash
docker-compose up -d backend
```

Backend běží na portu `http://localhost:8000`.

### 3. (Volitelné) Spusť migrations (pokud se strukturó db mění)

```bash
docker-compose up -d alembic
```

## API dokumentace

Po spuštění backendu otevři Swagger UI:

```bash
http://localhost:8000/docs
```

Nebo ReDoc:

```bash
http://localhost:8000/redoc
```

## Konfigurace

Používá environment variables:

| Variable            | Default (dev)              | Description                  |
|---------------------|---------------------------|------------------------------|
| DATABASE_HOST       | ai_operations_postgres    | PostgreSQL host              |
| DATABASE_PORT       | 5432                      | PostgreSQL port              |
| DATABASE_USER       | ai_user                   | PostgreSQL user              |
| DATABASE_PASSWORD   | ai_password               | PostgreSQL password          |
| DATABASE_NAME       | ai_operations             | Database name                |
| SECRET_KEY          | dev-secret-key            | JWT/session key              |
| ENVIRONMENT         | development              | development/production      |

Pro produkci:

```bash
docker-compose up -d postgres
docker-compose --env-file .env.production up -d backend
```

## Technologie

- **Python 3.12** + **uv** (dependency manager)
- **FastAPI** (web framework)
- **SQLAlchemy 2.0** (ORM, async)
- **Asyncpg** (async PostgreSQL driver)
- **Pydantic** (validation)
- **Docker** (containerizace)

## Následující kroky

1. Přidej SQLAlchemy models (`models.py`)
2. Přidej Pydantic schemas (`schemas.py`)
3. Implementuj API routes pro customers/orders
4. Přidej Alembic migrations
5. Přidej AI operations service

## License

© 2026 AI Operations Assistant Team