# api/services/ingestion_service.py
from pathlib import Path
from fastapi import HTTPException

from core.domain.ingest_logic import run_ingestion
from core.configs.settings import Settings

settings = Settings()


class IngestionService: 
    """API-facing wrapper for RAG ingestion."""

    def __init__(self, config_path: Path = None):
        self.config_path = config_path or Path(settings.LLM_CONFIG_PATH)

    def ingest_documents(self, input_file: Path = None) -> str:
        """
        Run ingestion and return vector store path.
        If input_file is provided, override the config in memory.
        """
        try:
            store_path = run_ingestion(self.config_path, input_file=input_file)
            return store_path

        except RuntimeError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error running ingestion: {str(e)}")
