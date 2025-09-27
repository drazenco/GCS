
# 🌌 Genesis Core Standard (GCS)

[![Build](https://github.com/drazenco/GCS/actions/workflows/python-tests.yml/badge.svg)](https://github.com/drazenco/GCS/actions/workflows/python-tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Status: Developer Preview](https://img.shields.io/badge/status-developer--preview-orange)

**Genesis Core Standard (GCS)** defines the **core API contract for AI memory systems**.  
It is the **specification repo** — the reference point for all Genesis components.

Our goal: to create an **“SQL for memories”** — stable, interoperable, and aligned with GDPR/AI Act rules.

---

## 🔑 Core (v0.1 — stable foundation)

**Invariant core operators** (mandatory in every version ≥ v0.1):

- `STORE` — store memory  
- `RECALL` — retrieve memory  
- `FORGET` — right to be forgotten  
- `CONSENT` — consent management  
- `EXPORT` — data transfer (NDJSON)

---

## 🧮 Version Evolution

```
v0.1  →  v0.2      →      v0.3         →        v1.0
CRUD+GDPR   +semantics     +distribution       +algebra
           (SUMMARY,EMBED) (SHARE, PIPE)    (PAR,CHECK, monoid)
```

- **v0.1** — stable core (CRUD + GDPR tools)  
- **v0.2** — semantic layer (embeddings, summary)  
- **v0.3** — distributed memory graph (sharing, pipelines)  
- **v1.0** — memory algebra (M, O, ∘) → monoid

---

## 📦 Ecosystem Repos

- **[Genesis-v2](https://github.com/drazenco/Genesis-v2)** — reference engine (FastAPI)  
- **[GMQL](https://github.com/drazenco/GMQL)** — query language for memory  
- **[LifeDB](https://github.com/drazenco/LifeDB)** — memory layer (SQLite → pgvector)  
- **[Rosetta](https://github.com/drazenco/Rosetta)** — privacy, consent, audit layer  
- **[GGA](https://github.com/drazenco/GGA)** — Genesis General Algebra  
- **[GAA](https://github.com/drazenco/GAA)** — Genesis Agent Algebra  
- **[Genesis-algebra](https://github.com/drazenco/Genesis-algebra)** — bridges GGA and GAA  
- **[Genesis-Rosetta](https://github.com/drazenco/Genesis-Rosetta)** — manifest / whitepaper  

All these repos **implement or extend GCS v0.1**.

---

## 🚀 Reference Template

📂 **gcs-template-v0.1** — starter kit for new repos:

- OpenAPI + JSON Schema  
- FastAPI reference server (SQLite)  
- Conformance kit (STORE/RECALL/FORGET/CONSENT/EXPORT tests)  
- Journal Bot demo (GDPR use-case)  
- Docker Compose + Makefile  

---

## ✅ Conformance

GCS provides the official **conformance kit**:  
Every implementation must pass the **STORE/RECALL/FORGET/CONSENT/EXPORT** test suite to claim compliance.

---

## 📜 License

MIT License — open for community use and contribution.  
⚠️ Developer Preview — not production ready.

---

💡 **Vision:**  
Genesis Core Standard aims to be for **AI memory** what SQL was for relational databases — a **unified language and API contract**, stable across versions, flexible for research, and robust for industry.
