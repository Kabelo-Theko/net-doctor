"""FastAPI server for net-doctor: serves the web UI and exposes the Python engine.

  GET  /api/flows           -> the diagnostic trees from net_doctor.flows
  POST /api/diagnose        -> replay a flow with a list of pass/fail answers
The web UI works fully on its own, but these endpoints let the same trees be
driven from the real Python module.

Run:
    pip install -r requirements.txt
    uvicorn web.server:app --reload
"""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from net_doctor.engine import run_flow
from net_doctor.flows import FLOWS

DOCS = Path(__file__).resolve().parent.parent / "docs"
app = FastAPI(title="net-doctor", version="0.1.0")


class DiagnoseRequest(BaseModel):
    flow: str
    answers: list[bool]


@app.get("/api/flows")
def flows():
    return FLOWS


@app.post("/api/diagnose")
def diagnose(req: DiagnoseRequest):
    result = run_flow(FLOWS[req.flow], req.answers, flow_key=req.flow)
    return {"path": result.path, "conclusion": result.conclusion}


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/")
def index():
    return FileResponse(DOCS / "index.html")


app.mount("/", StaticFiles(directory=DOCS, html=True), name="static")
