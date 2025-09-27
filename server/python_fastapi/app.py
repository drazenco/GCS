from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional, Any, Dict
from datetime import datetime, timezone
import sqlite3, json
from ulid import ULID

APP_VERSION = "GCS/0.1"
app = FastAPI(title="Genesis Core Standard (GCS) API", version="0.1.0")

def now_iso():
    return datetime.now(timezone.utc).isoformat()

def db():
    conn = sqlite3.connect("gcs.sqlite", check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    conn.execute("""CREATE TABLE IF NOT EXISTS memory_records(
        id TEXT PRIMARY KEY,
        tenant_id TEXT,
        subject_id TEXT,
        created_at TEXT,
        updated_at TEXT,
        type TEXT,
        content TEXT,
        tags TEXT,
        consent_ref TEXT,
        deleted_at TEXT DEFAULT NULL
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS consent_records(
        id TEXT PRIMARY KEY,
        subject_id TEXT,
        created_at TEXT,
        updated_at TEXT,
        grants TEXT
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS audit_events(
        id TEXT PRIMARY KEY,
        ts TEXT,
        actor TEXT,
        action TEXT,
        target_id TEXT,
        meta TEXT
    )""")
    return conn

CONN = db()

def audit(action:str, target_id:str, meta:Dict[str,Any]|None=None, actor:str="system"):
    ae_id = str(ULID())
    CONN.execute("INSERT INTO audit_events (id, ts, actor, action, target_id, meta) VALUES (?,?,?,?,?,?)",
                 (ae_id, now_iso(), actor, action, target_id, json.dumps(meta or {})))
    CONN.commit()

class StoreReq(BaseModel):
    tenant_id: str
    subject_id: str
    type: str
    content: Dict[str, Any]
    tags: Optional[List[str]] = None
    consent_ref: Optional[str] = None

class RecallReq(BaseModel):
    tenant_id: Optional[str] = None
    subject_id: Optional[str] = None
    type: Optional[str] = None
    tags: Optional[List[str]] = None
    q: Optional[str] = None
    limit: int = 20
    semantic: bool = False

class ForgetReq(BaseModel):
    id: str

class ConsentGrant(BaseModel):
    scope: str
    status: str

class ConsentRecord(BaseModel):
    id: str
    subject_id: str
    created_at: str
    updated_at: str
    grants: List[ConsentGrant]

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.get("/version")
def version():
    return {"version": APP_VERSION}

@app.post("/store")
def store(req: StoreReq, request: Request):
    rec_id = str(ULID())
    ts = now_iso()
    CONN.execute("""INSERT INTO memory_records
        (id, tenant_id, subject_id, created_at, updated_at, type, content, tags, consent_ref)
        VALUES (?,?,?,?,?,?,?,?,?)""",
        (rec_id, req.tenant_id, req.subject_id, ts, ts, req.type, json.dumps(req.content),
         json.dumps(req.tags or []), req.consent_ref))
    CONN.commit()
    audit("STORE", rec_id, {"path": str(request.url)})
    return {"id": rec_id}

@app.post("/recall")
def recall(req: RecallReq):
    sql = "SELECT id, tenant_id, subject_id, created_at, updated_at, type, content, tags, consent_ref FROM memory_records WHERE deleted_at IS NULL"
    params = []
    if req.tenant_id:
        sql += " AND tenant_id=?"; params.append(req.tenant_id)
    if req.subject_id:
        sql += " AND subject_id=?"; params.append(req.subject_id)
    if req.type:
        sql += " AND type=?"; params.append(req.type)
    if req.q:
        sql += " AND content LIKE ?"; params.append(f"%{req.q}%")
    if req.tags:
        for t in req.tags:
            sql += " AND tags LIKE ?"; params.append(f"%{t}%")
    sql += " ORDER BY created_at DESC LIMIT ?"; params.append(req.limit)
    rows = CONN.execute(sql, params).fetchall()
    items = []
    for r in rows:
        items.append({
            "id": r[0],
            "tenant_id": r[1],
            "subject_id": r[2],
            "created_at": r[3],
            "updated_at": r[4],
            "type": r[5],
            "content": json.loads(r[6]),
            "tags": json.loads(r[7] or "[]"),
            "consent_ref": r[8]
        })
    return {"items": items}

@app.post("/forget")
def forget(req: ForgetReq, request: Request):
    ts = now_iso()
    CONN.execute("UPDATE memory_records SET deleted_at=? WHERE id=?", (ts, req.id))
    CONN.commit()
    audit("FORGET", req.id, {"mode": "soft", "path": str(request.url)})
    return {"ok": True}

@app.post("/consent")
def consent(rec: ConsentRecord, request: Request):
    CONN.execute("""INSERT INTO consent_records (id, subject_id, created_at, updated_at, grants)
                    VALUES (?,?,?,?,?)
                    ON CONFLICT(id) DO UPDATE SET
                      subject_id=excluded.subject_id,
                      updated_at=excluded.updated_at,
                      grants=excluded.grants""",
                 (rec.id, rec.subject_id, rec.created_at, rec.updated_at, json.dumps([g.model_dump() for g in rec.grants])))
    CONN.commit()
    audit("CONSENT_UPDATE", rec.id, {"path": str(request.url)})
    return {"ok": True}

@app.post("/export")
def export(body: Dict[str, Any] = None):
    body = body or {}
    tenant_id = body.get("tenant_id")
    subject_id = body.get("subject_id")
    def gen():
        sql = "SELECT id, tenant_id, subject_id, created_at, updated_at, type, content, tags, consent_ref, deleted_at FROM memory_records WHERE 1=1"
        params = []
        if tenant_id:
            sql += " AND tenant_id=?"; params.append(tenant_id)
        if subject_id:
            sql += " AND subject_id=?"; params.append(subject_id)
        for r in CONN.execute(sql, params):
            obj = {
                "kind":"MemoryRecord",
                "id":r[0],"tenant_id":r[1],"subject_id":r[2],
                "created_at":r[3],"updated_at":r[4],"type":r[5],
                "content":json.loads(r[6]),"tags":json.loads(r[7] or "[]"),
                "consent_ref":r[8],"deleted_at":r[9]
            }
            yield json.dumps(obj) + "\n"
        for r in CONN.execute("SELECT id, ts, actor, action, target_id, meta FROM audit_events ORDER BY ts"):
            obj = {"kind":"AuditEvent","id":r[0],"ts":r[1],"actor":r[2],"action":r[3],"target_id":r[4],"meta":json.loads(r[5] or "{}")}
            yield json.dumps(obj) + "\n"
    return StreamingResponse(gen(), media_type="application/x-ndjson")
