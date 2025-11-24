from fastapi import APIRouter, HTTPException
from typing import List
from ..models import Quote, QuoteCreate, QuoteUpdate
from ..services.excel_service import excel_service

router = APIRouter()

@router.get("/quotes", response_model=List[Quote])
async def get_all_quotes():
    """Lista todos os orçamentos"""
    return excel_service.get_all_quotes()

@router.post("/quotes", response_model=Quote)
async def create_quote(quote: QuoteCreate):
    """Cria novo orçamento com análise de ML"""
    return excel_service.create_quote(quote)

@router.put("/quotes/{quote_id}", response_model=Quote)
async def update_quote(quote_id: int, quote_update: QuoteUpdate):
    """Atualiza um orçamento existente"""
    updated_quote = excel_service.update_quote(quote_id, quote_update)
    if not updated_quote:
        raise HTTPException(status_code=404, detail="Orçamento não encontrado")
    return updated_quote

@router.delete("/quotes/{quote_id}")
async def delete_quote(quote_id: int):
    """Exclui um orçamento"""
    success = excel_service.delete_quote(quote_id)
    if not success:
        raise HTTPException(status_code=404, detail="Orçamento não encontrado")
    return {"message": "Orçamento excluído com sucesso"}
