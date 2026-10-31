"""Main FastAPI application entrypoint for TaskGuard."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.models.schemas import HealthResponse
from app.routers import analyze, eval_router, report
from app.services.llm_service import get_llm_service
from app.services.mca_lookup import get_mca_service

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("taskguard")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: preload cache and checks
    settings = get_settings()
    logger.info("Initializing TaskGuard Backend (CT BuildFest 2.0 - CTBF-AI-11)...")
    mca = get_mca_service()
    logger.info(f"Loaded {len(mca._cached_companies)} MCA company records into memory.")
    llm = get_llm_service()
    logger.info(f"Gemini LLM configured: {llm.is_configured}")
    yield
    logger.info("TaskGuard backend shutting down.")


settings = get_settings()

app = FastAPI(
    title="TaskGuard API",
    description="Scam-Stage Radar for Task Scams & Fake Job Offers (CT BuildFest 2.0)",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS setup for Vite frontend (localhost:5173 / localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Open during hackathon demo for easy multi-device testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(analyze.router)
app.include_router(report.router)
app.include_router(eval_router.router)


@app.get("/api/health", response_model=HealthResponse, tags=["System"])
async def health_check() -> HealthResponse:
    """System health check and LLM readiness."""
    llm = get_llm_service()
    return HealthResponse(
        status="ok",
        version="1.0.0",
        gemini_configured=bool(llm._gemini_client),
        groq_configured=bool(llm.groq_api_key),
        llm_provider=llm.provider_name,
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
