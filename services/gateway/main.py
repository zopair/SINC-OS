from fastapi import FastAPI, Request
import httpx, time, uuid, structlog
from tenacity import retry, stop_after_attempt, wait_exponential
from pybreaker import CircuitBreaker

structlog.configure()
logger = structlog.get_logger()
app = FastAPI(title="SINC Resilient Gateway")
db_breaker = CircuitBreaker(fail_max=5, reset_timeout=60)

@app.middleware("http")
async def resilience_middleware(request: Request, call_next):
    correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info("request_processed", path=request.url.path, duration=duration, correlation_id=correlation_id)
    return response

@app.get("/orchestrator/health")
async def proxy_health():
    async with httpx.AsyncClient() as client:
        return (await client.get("http://127.0.0.1:8001/health")).json()
