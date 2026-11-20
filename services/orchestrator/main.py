"""Minimal health surface for the SINC-OS orchestrator."""

import structlog
from fastapi import FastAPI

structlog.configure()
logger = structlog.get_logger()
app = FastAPI(title="SINC Stateful Orchestrator")


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "orchestrator",
        "persistence": "not_configured",
    }
