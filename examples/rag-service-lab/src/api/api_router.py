"""API routes package."""

from fastapi import APIRouter

from .routes import ingest_endpoint, chat_endpoint, config_endpoint


router = APIRouter()
router.include_router(ingest_endpoint.router)
router.include_router(chat_endpoint.router)
router.include_router(config_endpoint.router)