"""HTTP gateway for the SINC-OS orchestrator."""

import os
import time
import uuid

import httpx
import structlog
from fastapi import FastAPI, HTTPException, Request

structlog.configure()
logger = structlog.get_logger()
app = FastAPI(title="SINC Resilient Gateway")


@app.middleware("http")
async def resilience_middleware(request: Request, call_next):
    correlation_id = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
    started_at = time.monotonic()
    response = await call_next(request)
    response.headers["X-Correlation-ID"] = correlation_id
    logger.info(
        "request_processed",
        path=request.url.path,
        duration_seconds=round(time.monotonic() - started_at, 6),
        correlation_id=correlation_id,
    )
    return response


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "gateway"}


@app.get("/orchestrator/health")
async def proxy_health():
    upstream = os.getenv("ORCHESTRATOR_URL", "http://orchestrator:8001").rstrip("/")
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{upstream}/health")
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as exc:
        logger.warning("orchestrator_unavailable", error_type=type(exc).__name__)
        raise HTTPException(status_code=503, detail="Orchestrator is unavailable") from exc
