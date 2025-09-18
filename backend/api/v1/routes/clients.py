from fastapi import APIRouter
from typing import List
from ..models import Client, ClientCreate
from ..services.excel_service import excel_service

router = APIRouter()

@router.get("/clients", response_model=List[Client])
async def get_all_clients():
    """Lista todos os clientes"""
    return excel_service.get_all_clients()

@router.post("/clients", response_model=Client)
async def create_client(client: ClientCreate):
    """Cria novo cliente"""
    return excel_service.create_client(client)
