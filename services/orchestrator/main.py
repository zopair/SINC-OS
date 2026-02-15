from fastapi import FastAPI
import structlog
logger = structlog.get_logger()
app = FastAPI(title="SINC Stateful Orchestrator")
@app.get("/health")
async def health():
    return {"status": "healthy", "engine": "stateful_streams", "persistence": "enabled"}
