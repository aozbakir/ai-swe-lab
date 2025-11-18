from fastapi import APIRouter
from ..services.config_service import ConfigService

router = APIRouter()
config_service = ConfigService()

@router.get("/config")
def get_config():
    return config_service.get_config_params()