from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Modelos para Clientes
class ClientBase(BaseModel):
    name: str

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    name: Optional[str] = None

class Client(ClientBase):
    id: int
    created_at: datetime
    updated_at: datetime
