from fastapi import APIRouter
from typing import List
from ..models import Service, ServiceCreate
from ..services.excel_service import excel_service

router = APIRouter()

@router.get("/services", response_model=List[Service])
async def get_all_services():
    """Lista todos os serviços residenciais"""
    return excel_service.get_all_services()

@router.post("/services", response_model=Service)
async def create_service(service: ServiceCreate):
    """Cria novo serviço com categorização automática"""
    return excel_service.create_service(service)
