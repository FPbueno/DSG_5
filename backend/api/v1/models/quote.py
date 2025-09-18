from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .client import Client
from .service import Service

# Modelos para Itens do Orçamento
class QuoteItemBase(BaseModel):
    service_id: int
    quantity: float
    unit_price: float

class QuoteItemCreate(QuoteItemBase):
    pass

class QuoteItemUpdate(BaseModel):
    quantity: Optional[float] = None
    unit_price: Optional[float] = None

class QuoteItem(QuoteItemBase):
    id: int
    total_price: float
    service_name: str
    service_unit: str

# Modelos para Orçamentos
class QuoteBase(BaseModel):
    client_id: int
    title: str
    description: Optional[str] = None
    status: str = "draft"  # draft, sent, approved, rejected

class QuoteCreate(QuoteBase):
    items: List[QuoteItemCreate] = []

class QuoteUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    items: Optional[List[QuoteItemCreate]] = None

class Quote(QuoteBase):
    id: int
    quote_number: str
    total: float
    created_at: datetime
    updated_at: datetime
    client: Client
    items: List[QuoteItem]

    class Config:
        from_attributes = True
