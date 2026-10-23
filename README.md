# AI Operations Assistant

Backend API postavené na FastAPI, asynchronním SQLAlchemy a PostgreSQL. Schéma ORM tabulek spravuje Alembic.

## Způsob práce

- Python, uv, FastAPI, SQLAlchemy a Alembic běží pouze v Dockeru. Lokální Python ani `.venv` nejsou potřeba.
- Zdrojové soubory i všechny migrace jsou uložené na macOS v projektu a verzované v Gitu.
- Backend nemá bind mount zdrojových souborů. Dockerfile při buildu kopíruje backend, migrace a `alembic.ini` do `/app`.
- Závislosti včetně Alembicu se instalují do image pomocí `uv sync --locked` podle `pyproject.toml` a `uv.lock`.
- Po změně zdrojových souborů, závislostí nebo migrací je potřeba backend znovu sestavit.

## Struktura projektu

```text
ai_operations_assistant/
├── backend/
│   ├── main.py                    # Alternativní spouštěcí modul
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                # FastAPI aplikace; vstupní bod Dockeru
│   │   ├── config.py              # Konfigurace z proměnných prostředí
│   │   ├── database.py            # Async engine a databázové sessions
│   │   ├── models.py              # ORM Base a model Test
│   │   ├── schemas.py             # Pydantic schémata API
│   │   └── routers/
│   │       ├── __init__.py
│   │       ├── health.py
│   │       └── test.py            # CRUD pro záznamy tests
│   └── alembic/
│       ├── README
│       ├── env.py                 # Async připojení a filtr spravovaných tabulek
│       ├── script.py.mako         # Šablona migračních revizí
│       └── versions/
│           ├── 5d3c5b71f797_initial_create_tests.py
│           └── 6f536185102a_add_email_to_tests.py
├── docker/
│   ├── postgres/init.sql          # Inicializace customers a orders
│   └── backend/Dockerfile
├── .dockerignore                 # Vyloučení lokálního prostředí a cache z buildu
├── .gitignore                    # Vyloučení __pycache__ z Gitu
├── alembic.ini                   # Konfigurace Alembicu a cesta k migracím
├── docker-compose.yaml
├── pyproject.toml
├── uv.lock
└── README.md
```

## Spuštění

Předpoklady: Docker Desktop s Docker Compose a volné porty 8000 a 5432. Příkazy spouštěj z kořenového adresáře projektu.

```bash
docker compose up -d --build backend
```

Compose spustí také PostgreSQL a před startem backendu počká na jeho úspěšný healthcheck. Vstupní bod aplikace je `backend.app.main:app`.

Backend při startu ověřuje připojení pomocí `SELECT 1`. Tabulky nevytváří a migrace automaticky nespouští. Na nové databázi je před použitím CRUD API potřeba aplikovat migrace podle následující části.

- Backend: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Kontrola backendu a připojení k databázi: http://localhost:8000/api/v1/health/

## Databáze a Alembic

PostgreSQL 18 ukládá data do pojmenovaného volume `postgres_data`. Skript `docker/postgres/init.sql` se provádí pouze při inicializaci prázdného datového adresáře. Vytváří tabulky `customers`, `orders` a jejich ukázková data; tabulku `tests` nevytváří.

Alembic získává URL připojení z `Config` v `backend/app/config.py` a používá `postgresql+asyncpg`. ORM modely se registrují importem `backend.app.models`; `Base.metadata` určuje požadované schéma. Filtr `include_name` omezuje autogenerate na schémata a tabulky z těchto metadat. Nespravované tabulky, například `customers` a `orders`, se neporovnávají k odstranění. Každý návrh migrace přesto ručně zkontroluj.

Řetězec migrací:

| Revize | Předchozí revize | Změna |
|---|---|---|
| `5d3c5b71f797` | žádná | Vytvoření tests: id, jmeno, prijmeni |
| `6f536185102a` | `5d3c5b71f797` | Přidání nullable email VARCHAR(255) |

Aktuální revize databáze se může lišit od poslední dostupné migrace. Ověř ji v běžícím backendu:

```bash
docker compose exec backend uv run --locked alembic --version
docker compose exec backend uv run --locked alembic history
docker compose exec backend uv run --locked alembic current
```

### Nová databáze bez tabulky tests

Po sestavení image a spuštění PostgreSQL lze aplikovat celý řetězec:

```bash
docker compose run --rm --no-deps backend uv run --locked alembic upgrade head
```

Tento příkaz mění databázové schéma. Služba PostgreSQL musí být spuštěná; `--no-deps` ji nespouští. Stejný způsob lze použít pro kontrolní příkazy, pokud backend neběží.

### Existující databáze s daty v tests

Nejdřív vytvoř zálohu, ověř `alembic current` a porovnej skutečné schéma s migracemi. Výchozí migraci vytvářející `tests` neaplikuj na již existující tabulku.

Pouze pokud databáze ještě nemá evidovanou revizi a její tabulka `tests` přesně odpovídá první migraci, lze výchozí stav zaznamenat:

```bash
docker compose exec backend uv run --locked alembic stamp 5d3c5b71f797
```

`stamp` zapisuje evidenci revize, ale neprovádí změny popsané migrací. Nepoužívej jej k přeskočení chybějících změn schématu. Pokud je databáze již na první revizi, neopakuj jej. Před aplikací další migrace ověř, zda sloupec `email` již existuje a zda skutečné schéma odpovídá evidované revizi.

### Vytvoření a uchování dalších migrací

Po změně ORM modelu znovu sestav backend, aby kontejner obsahoval aktuální modely. Pro autogenerate musí databáze odpovídat dosavadnímu migračnímu řetězci.

```bash
docker compose exec backend uv run --locked alembic revision --autogenerate -m "popis zmeny"
```

Pro ručně psanou revizi vynech `--autogenerate`. Nový soubor vznikne uvnitř kontejneru. **Před jeho odstraněním nebo obnovením zkopíruj migraci na macOS**; nahraď `NAZEV_SOUBORU.py` skutečným názvem:

```bash
docker cp ai_operations_backend:/app/backend/alembic/versions/NAZEV_SOUBORU.py backend/alembic/versions/NAZEV_SOUBORU.py
```

Pokud cílový soubor již existuje, nejdřív porovnej obsah. Zkontroluj operace i `down_revision`, zařaď soubor do Gitu a znovu sestav backend:

```bash
docker compose up -d --build backend
```

Samotné sestavení ani start kontejneru migraci neaplikují. Změny v databázi prováděj až po kontrole migrace a záloze. Do Gitu patří soubory `.py`, nikoli `__pycache__`.

## API

| Metoda | Cesta | Účel |
|---|---|---|
| GET | `/` | Informace o aplikaci |
| GET | `/api/v1/health/` | Kontrola připojení k databázi |
| GET | `/api/v1/test/` | Seznam záznamů |
| POST | `/api/v1/test/` | Vytvoření záznamu |
| GET | `/api/v1/test/{test_id}` | Detail záznamu |
| PUT | `/api/v1/test/{test_id}` | Úprava záznamu |
| DELETE | `/api/v1/test/{test_id}` | Odstranění záznamu |

Vstup pro vytvoření a úpravu záznamu obsahuje `jmeno` a `prijmeni`. Odpověď obsahuje také `id`. Sloupec `email` je definovaný v ORM modelu a druhé migraci, ale zatím není vystavený v Pydantic schématech ani API.

## Konfigurace

`Config` čte proměnné prostředí. Compose nyní předává pevně zadané vývojové hodnoty:

| Proměnná | Výchozí hodnota v Config / hodnota v Compose |
|---|---|
| DATABASE_HOST | ai_operations_postgres |
| DATABASE_PORT | 5432 |
| DATABASE_USER | ai_user |
| DATABASE_PASSWORD | ai_password |
| DATABASE_NAME | ai_operations |
| SECRET_KEY | dev-secret-key-change-in-production |
| ENVIRONMENT | development |

Uvnitř Docker sítě backend používá host `ai_operations_postgres`. PostgreSQL je také dostupný z macOS na `localhost:5432` pro externí databázové nástroje.

Současný Compose je určen pro vývoj. Samotné `--env-file .env.production` nepřepíše hodnoty natvrdo uvedené v `environment`. Pro produkční nasazení je potřeba nejprve upravit předávání konfigurace a tajných údajů, omezit CORS a nastavit odpovídající provozní zabezpečení. Současná konfigurace není hotový produkční deployment.

## Provozní příkazy

```bash
# Stav kontejnerů
docker compose ps

# Logy backendu
docker compose logs -f backend

# Logy PostgreSQL
docker compose logs -f postgres

# Zastavení a odstranění kontejnerů se zachováním databázového volume
docker compose down
```

`docker compose down -v` odstraní také databázový volume a jeho data; nepoužívej jej při běžném zastavení projektu.

## Technologie a další rozvoj

- Python 3.12 v Docker image, uv, FastAPI, Pydantic.
- SQLAlchemy 2 s asyncio, asyncpg, PostgreSQL 18 a Alembic.
- Pytest, pytest-asyncio a HTTPX jsou v závislostech; automatická testovací sada zatím není vytvořená. `routers/test.py` je API router.
- Další rozvoj: zpřístupnění emailu v API, automatické testy, ORM/API pro customers a orders a AI operations service.
- Frontend zatím není implementovaný.

## License

© 2026 AI Operations Assistant Team
