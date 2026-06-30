from fastapi import Depends, FastAPI

from . import db, repository, store, templates, worker
from .auth import require_api_key
from .models import GenerateRequest, RegenerateRequest, SetTemplateRequest

app = FastAPI(title="creative-gen")


@app.post("/generate")
def generate(req: GenerateRequest, tenant: str = Depends(require_api_key)):
    c = worker.generate(req)
    return {"item_id": c.item_id, "caption": c.caption, "hook": c.hook}


@app.post("/regenerate")
def regenerate(req: RegenerateRequest, tenant: str = Depends(require_api_key)):
    c = worker.regenerate(req)
    return {"item_id": c.item_id, "caption": c.caption, "hook": c.hook}


@app.post("/template")
def set_template(req: SetTemplateRequest, tenant: str = Depends(require_api_key)):
    templates.set_template(req.creator_id, req.template)
    return {"ok": True}


@app.get("/items")
def list_items(offset: int = 0, limit: int = 5, tenant: str = Depends(require_api_key)):
    rows = store.list_recent(offset, limit)
    return {"items": [{"item_id": r.item_id, "performance": r.performance} for r in rows]}


@app.get("/creators/{creator_id}/items")
def creator_items(creator_id: str, tenant: str = Depends(require_api_key)):
    rows = repository.list_by_creator(creator_id)
    return {"items": [{"item_id": r.item_id} for r in rows if r]}


@app.get("/healthz")
def healthz():
    return {"ok": True, "db_items": db.count_items()}


@app.on_event("startup")
def _startup():
    db.init_db()
