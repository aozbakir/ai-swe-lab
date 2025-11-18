# api/routes/ingest_endpoint.py
from pathlib import Path
import tempfile

from fastapi import APIRouter, UploadFile, Depends

from api.services.ingest_service import IngestionService

router = APIRouter(tags=["ingest"])

def get_ingestion_service() -> IngestionService:
    return IngestionService()

@router.post("/ingest")
async def ingest_file(file: UploadFile, service: IngestionService = Depends(get_ingestion_service)):
    """
    Upload a PDF and run the RAG ingestion pipeline.
    Returns path to the created vector store.
    """
    # Save uploaded PDF to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        temp_path = Path(tmp.name)
        tmp.write(await file.read())

    try:
        # Run ingestion with uploaded PDF
        store_path = service.ingest_documents(input_file=temp_path)
    finally:
        # Clean up temporary file
        temp_path.unlink(missing_ok=True)

    return {"status": "ok", "vector_store_path": store_path}
