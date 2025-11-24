from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Modelos para Serviços Residenciais
class ServiceBase(BaseModel):
    name: str
    unit_price: float
    unit: str = "h"  # h (horas), un (unidade), m² (metro quadrado)

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    unit_price: Optional[float] = None
    unit: Optional[str] = None

class Service(ServiceBase):
    id: int
    created_at: datetime
    updated_at: datetime
