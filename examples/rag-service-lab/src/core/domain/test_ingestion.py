from pathlib import Path
from ingest_logic import run_ingestion

def test_ingestion():
    config_path = Path("core/configs/config.yaml")
    try:
        vector_store_path = run_ingestion(config_path)
        print(f"Ingestion succeeded! Vector store at: {vector_store_path}")
    except Exception as e:
        print(f"Ingestion failed: {e}")

if __name__ == "__main__":
    test_ingestion()
