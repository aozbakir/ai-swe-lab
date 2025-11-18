# src/main.py
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from src.api.api_router import router as api_router
from src.core.configs.settings import Settings

# LLM imports instantiation logic
from llm_utils.factory_protocol import LLMFactory


PROJECT_ROOT = Path(__file__).resolve().parent

settings = Settings()


# ------------------------------------------------------------
# Lifespan: load LLM + config ONCE (singleton)
# ------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize LLM once
    factory = LLMFactory()
    llm = factory.create_from_yaml(settings.LLM_CONFIG_PATH, agentic=False)
    app.state.llm = llm
    app.state.settings = settings

    yield
    # --- Shutdown ---


# ------------------------------------------------------------
# App creation
# ------------------------------------------------------------
app = FastAPI(
    title="RAG Ingestion + Chat Service",
    lifespan=lifespan
)


# ------------------------------------------------------------
# Routers
# ------------------------------------------------------------
app.include_router(api_router)


# ------------------------------------------------------------
# Static Files
# ------------------------------------------------------------
app.mount("/static", StaticFiles(directory=PROJECT_ROOT / "static"), name="static")


# ------------------------------------------------------------
# Root = index.html
# ------------------------------------------------------------
@app.get("/", include_in_schema=False)
def root():
    return FileResponse(PROJECT_ROOT / "static" / "index.html")
