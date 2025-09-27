# Genesis Core Standard (GCS) v0.1 — Template

A thin, stable foundation that unifies **GMQL / Genesis v2** repos with a single API contract
and conformance tests. Use this template for new adapters, SDKs, or demos.

## What you get
- **OpenAPI** + **JSON Schemas** for `MemoryRecord`, `ConsentRecord`, `AuditEvent`.
- Minimal **FastAPI** reference server (`/server/python_fastapi`) using SQLite.
- **Conformance kit** to validate STORE / RECALL / FORGET / CONSENT / EXPORT behavior.
- A tiny **Journal Bot** demo (static HTML) hitting the API to showcase GDPR flows.
- **Docker Compose** + Makefile for one‑command run.

## API contract (GCS v0.1)
- `POST /store`
- `POST /recall`
- `POST /forget`
- `POST /consent`
- `POST /export` (NDJSON stream)
- `GET /healthz`
- `GET /version`

## Quickstart
```bash
make up           # build & run via Docker
# or local:
python -m venv .venv && source .venv/bin/activate
pip install -r server/python_fastapi/requirements.txt
uvicorn server.python_fastapi.app:app --reload
```

Open the demo at `examples/journal_bot/index.html` (serve it via any static server or open directly).

## Conformance
```bash
# run a local server on http://127.0.0.1:8000 first
python conformance/runner.py --base http://127.0.0.1:8000
```

## 📦 Repo Ecosystem

- **[GMQL](./GMQL)** — query language for memory  
- **[Genesis-v2](./Genesis-v2)** — reference engine (FastAPI)  
- **[LifeDB](./LifeDB)** — memory layer (SQLite → pgvector)  
- **[Rosetta](./Rosetta)** — privacy, consent, audit layer  
- **[GGA](./GGA)** — Genesis General Algebra  
- **[GAA](./GAA)** — Genesis Agent Algebra  
- **[Genesis-algebra](./Genesis-algebra)** — bridges GGA and GAA  
- **[Genesis-Rosetta](./Genesis-Rosetta)** — manifest / whitepaper  

👉 All repos implement or extend the **GCS v0.1 template**.

## License
MIT
